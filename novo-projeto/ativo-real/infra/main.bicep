targetScope = 'resourceGroup'

@description('Nome do projeto para naming')
param projectName string = 'ativoreal'

@description('Ambiente (dev, staging, production)')
param environment string = 'production'

@description('Centro de custo')
param costCenter string = 'ativo-real-app'

@description('Região do Azure')
param location string = resourceGroup().location

@description('Habilitar Application Insights')
param enableMonitoring bool = true

param monitoringToolParameters object = appInsights

// Gerar sufixo único
var resourceSuffix = uniqueString(resourceGroup().id)

// Nomes dos recursos
var cosmosDbAccountName = '${projectName}-cosmos-${resourceSuffix}'
var cosmosDbDatabaseName = 'AtivoRealDB'
var staticWebAppName = '${projectName}-web-${resourceSuffix}'
var functionAppName = '${projectName}-api-${resourceSuffix}'
var storageAccountName = '${projectName}st${resourceSuffix}'
var appServicePlanName = '${projectName}-plan-${resourceSuffix}'
var appInsightsName = '${projectName}-insights-${resourceSuffix}'
var logAnalyticsName = '${projectName}-logs-${resourceSuffix}'
var redisCacheName = '${projectName}-redis-${resourceSuffix}'

// Tags comuns
var commonTags = {
  project: projectName
  environment: environment
  costCenter: costCenter
  managedBy: 'bicep'
}

// ========================================
// Log Analytics Workspace
// ========================================
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  tags: commonTags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ========================================
// Application Insights
// ========================================
resource appInsights 'Microsoft.Insights/components@2020-02-02' = if (enableMonitoring) {
  name: appInsightsName
  location: location
  kind: 'web'
  tags: commonTags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
  }
}

// ========================================
// Azure Cosmos DB (NoSQL API)
// ========================================
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
        isZoneRedundant: false
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    enableFreeTier: false
    publicNetworkAccess: 'Enabled'
    ipRules: []
    isVirtualNetworkFilterEnabled: false
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
        includedPaths: [
          { path: '/*' }
        ]
        excludedPaths: [
          { path: '/"_etag"/?' }
        ]
        spatialIndexes: [
          {
            path: '/location/*'
            types: ['Point', 'Polygon']
          }
        ]
      }
      uniqueKeyPolicy: {
        uniqueKeys: [
          {
            paths: ['/document']
          }
        ]
      }
    }
  }
}

// Container: Propriedades Urbanas
resource urbanPropertiesContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: cosmosDatabase
  name: 'UrbanProperties'
  properties: {
    resource: {
      id: 'UrbanProperties'
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

// Container: Usuários/Técnicos
resource usersContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: cosmosDatabase
  name: 'Users'
  properties: {
    resource: {
      id: 'Users'
      partitionKey: {
        paths: ['/tenantId']
        kind: 'Hash'
      }
      uniqueKeyPolicy: {
        uniqueKeys: [
          {
            paths: ['/cpf']
          }
          {
            paths: ['/email']
          }
        ]
      }
    }
  }
}

// Container: Logs de Auditoria
resource auditLogsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: cosmosDatabase
  name: 'AuditLogs'
  properties: {
    resource: {
      id: 'AuditLogs'
      partitionKey: {
        paths: ['/tenantId', '/userId']
        kind: 'MultiHash'
        version: 2
      }
      defaultTtl: 2592000 // 30 dias
    }
  }
}

// ========================================
// Azure Cache for Redis
// ========================================
resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: redisCacheName
  location: location
  tags: commonTags
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
  }
}

// ========================================
// Storage Account (para Functions)
// ========================================
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: commonTags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

// ========================================
// App Service Plan (Consumption Y1)
// ========================================
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  tags: commonTags
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {}
}

// ========================================
// Azure Functions App
// ========================================
@batchSize()
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: functionAppName
  location: location
  tags: commonTags
  kind: 'functionapp,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    reserved: true
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'Python|3.11'
      appSettings: [
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${az.environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'COSMOS_DB_ENDPOINT'
          value: cosmosDbAccount.properties.documentEndpoint
        }
        {
          name: 'COSMOS_DB_KEY'
          value: cosmosDbAccount.listKeys().primaryMasterKey
        }
        {
          name: 'COSMOS_DB_DATABASE'
          value: cosmosDbDatabaseName
        }
        {
          name: 'REDIS_CONNECTION_STRING'
          value: '${redisCacheName}.redis.cache.windows.net:6380,password=${redisCache.listKeys().primaryKey},ssl=True,abortConnect=False'
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: enableMonitoring && monitoringToolParameters != null ? appInsights.properties.ConnectionString : ''
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ]
      cors: {
        allowedOrigins: [
          'https://${staticWebAppName}.azurestaticapps.net'
          'http://localhost:5173'
        ]
        supportCredentials: true
      }
    }
  }
}

// ========================================
// Static Web App (Frontend)
// ========================================
resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' = {
  name: staticWebAppName
  location: 'eastus2' // Static Web Apps tem regiões limitadas
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

// ========================================
// Role Assignments (Managed Identity)
// ========================================
resource cosmosDbDataContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(cosmosDbAccount.id, functionApp.id, 'CosmosDBDataContributor')
  scope: cosmosDbAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '00000000-0000-0000-0000-000000000002')
    principalId: functionApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// ========================================
// Outputs
// ========================================
output staticWebAppUrl string = 'https://${staticWebApp.properties.defaultHostname}'
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
output cosmosDbEndpoint string = cosmosDbAccount.properties.documentEndpoint
output cosmosDbConnectionString string = 'AccountEndpoint=${cosmosDbAccount.properties.documentEndpoint};AccountKey=${cosmosDbAccount.listKeys().primaryMasterKey};'
output redisConnectionString string = '${redisCacheName}.redis.cache.windows.net:6380,password=${redisCache.listKeys().primaryKey},ssl=True'
output appInsightsConnectionString string = enableMonitoring && appInsights != null ? appInsights.properties.ConnectionString : ''
output resourceGroupName string = resourceGroup().name
