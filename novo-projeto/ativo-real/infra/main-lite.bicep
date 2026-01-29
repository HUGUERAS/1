targetScope = 'resourceGroup'

param projectName string = 'ativoreal'
param envName string = 'production'
param costCenter string = 'ativo-real-app'
param location string = resourceGroup().location

var resourceSuffix = uniqueString(resourceGroup().id)
var cosmosDbAccountName = '${projectName}-cosmos-${resourceSuffix}'
var cosmosDbDatabaseName = 'AtivoRealDB'
var staticWebAppName = '${projectName}-web-${resourceSuffix}'

var commonTags = {
  project: projectName
  environment: envName
  costCenter: costCenter
}

// Cosmos DB
resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: cosmosDbAccountName
  location: location
  tags: commonTags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
  }
}

resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmosDbAccount
  name: cosmosDbDatabaseName
  properties: {
    resource: {
      id: cosmosDbDatabaseName
    }
  }
}

// Container: Propriedades Rurais
resource ruralPropertiesContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: cosmosDatabase
  name: 'RuralProperties'
  properties: {
    resource: {
      id: 'RuralProperties'
      partitionKey: {
        paths: ['/tenantId']
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        spatialIndexes: [
          {
            path: '/location/*'
            types: ['Point', 'Polygon']
          }
        ]
      }
    }
  }
}

// Static Web App
resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' = {
  name: staticWebAppName
  location: location
  tags: commonTags
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {
    buildProperties: {
      appLocation: '/ativo-real'
      outputLocation: 'dist'
    }
  }
}

output staticWebAppUrl string = 'https://${staticWebApp.properties.defaultHostname}'
output cosmosDbEndpoint string = cosmosDbAccount.properties.documentEndpoint
output cosmosDbKey string = cosmosDbAccount.listKeys().primaryMasterKey
