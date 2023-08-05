declare var window


export function initDjangoEnv() {
    window.DJANGO = {
        user: {isAuthenticated: true},
        priceRange: {min: 100, max: 30000},
    }
}
