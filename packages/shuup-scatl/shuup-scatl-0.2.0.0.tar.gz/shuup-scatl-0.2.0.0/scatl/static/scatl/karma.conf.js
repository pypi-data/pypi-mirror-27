module.exports = function(config) {
    config.set({
        basePath: '.',
        
        frameworks: ['jasmine'],
        
        files: [
            // systemjs for module loading
            'node_modules/systemjs/dist/system.src.js',
            
            // zone.js dependencies
            'node_modules/zone.js/dist/zone.js',
            'node_modules/zone.js/dist/proxy.js',
            'node_modules/zone.js/dist/sync-test.js',
            'node_modules/zone.js/dist/jasmine-patch.js',
            'node_modules/zone.js/dist/async-test.js',
            'node_modules/zone.js/dist/fake-async-test.js',

            'node_modules/faker/build/build/faker.js',

            'systemjs.conf.spec.js',
            'karma.shim.js',

            // paths loaded via module imports

            {pattern: 'node_modules/rxjs/**/*.js', included: false, watched: false},
            {pattern: 'node_modules/rxjs/**/*.js.map', included: false, watched: false},

            // angular itself
            'node_modules/reflect-metadata/Reflect.js',
            {pattern: 'node_modules/@angular/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/@angular/**/*.js.map', included: false, watched: true},
            {pattern: 'node_modules/traceur/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/traceur/**/*.js.map', included: false, watched: true},

            // angular2-notifications
            {pattern: 'node_modules/angular2-notifications/**/*.js', included: false, watched: true},

            // nouislider
            {pattern: 'node_modules/nouislider/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/ng2-nouislider/**/*.js', included: false, watched: true},

            // ng2-slim-loading-bar
            {pattern: 'node_modules/ng2-slim-loading-bar/**/*.js', included: false, watched: true},

            {pattern: 'app/**/*.js', included: false, watched: true},
            {pattern: 'app/**/*.ts', included: false, watched: false},
            {pattern: 'app/**/*.js.map', included: false, watched: false},
            {pattern: 'app/**/*.html', included: false, watched: true},
            {pattern: 'app/**/*.css', included: false, watched: true},
            {pattern: 'testutils/**/*.js', included: false, watched: true},
            {pattern: 'testutils/**/*.js.map', included: false, watched: true},
        ],

        proxies: {
            // required for component assets fetched by angular compiler
            '/app/': '/base/app/'
        },

        reporters: ['progress'],
        port: 9876,
        colors: true,
        logLevel: config.LOG_INFO,
        autoWatch: false,
        browsers: ['Firefox'],
        customLaunchers: {
            chrome_karma: {
                base: 'Chrome',
                flags: ['--user-data-dir=./.browsers/karma-chrome'],
            },
        },
        browserNoActivityTimeout: 30000,
        singleRun: true,
   })
}
