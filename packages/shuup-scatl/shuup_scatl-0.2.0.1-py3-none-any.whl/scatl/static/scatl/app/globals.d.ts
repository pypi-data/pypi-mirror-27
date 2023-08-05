// noinspection JSUnusedGlobalSymbols
interface Window {
    DJANGO: DjangoProvidedGlobals
}


interface DjangoProvidedGlobals {
    user: {
        isAuthenticated: boolean
        username?: string
    }
    priceRange: {
        min: number
        max: number
    }
    staticUrl: string
}
