declare module 'togeojson' {
  export function kml(doc: Document): unknown
  export function gpx(doc: Document): unknown
}

declare module 'papaparse' {
  const Papa: any
  export default Papa
}
