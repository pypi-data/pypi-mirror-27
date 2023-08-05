exports.config = {
    framework: 'jasmine',
    useAllAngular2AppRoots: true,
    capabilities: {
        browserName: 'chrome',
        chromeOptions: {
            'args': [
                '--user-data-dir=./.browsers/protractor-chrome',
                '--no-sandbox',
                '--aggressive-cache-discard',
                '--disable-cache',
                '--disable-application-cache',
                '--disable-offline-load-stale-cache',
                '--disk-cache-size=0',
            ],
        },
    },
    specs: [
        './e2e/attrim-form.comp.e2e-spec.js',
        './e2e/price-range-form.comp.e2e-spec.js',
        './e2e/sorting-form.comp.e2e-spec.js',
        './e2e/router.e2e-spec.js',
    ],
    seleniumServerJar: './node_modules/selenium-server-standalone-jar/jar/selenium-server-standalone-3.7.1.jar',
    SELENIUM_PROMISE_MANAGER: false,
}
