"use strict";
var specConfig;
(function (specConfig) {
    function build() {
        let config = {
            baseURL: '/base',
            paths: {
                'npm:': 'node_modules/'
            },
            map: {},
            packages: {
                '.': {
                    defaultJSExtensions: 'js'
                },
                'app': {
                    defaultExtension: 'js',
                },
            },
        };
        addAngularCore(config);
        addAngularTesting(config);
        addRxjs(config);
        addNgNotifications(config);
        addNgNouislider(config);
        addFaker(config);
        addNgSlimLoadingBar(config);
        return config;
    }
    specConfig.build = build;
    function addAngularCore(config) {
        let packages = {
            '@angular/animations': '@angular/animations/bundles/animations',
            '@angular/animations/browser': '@angular/animations/bundles/animations-browser',
            '@angular/core': '@angular/core/bundles/core',
            '@angular/common': '@angular/common/bundles/common',
            '@angular/compiler': '@angular/compiler/bundles/compiler',
            '@angular/http': '@angular/http/bundles/http',
            '@angular/router': '@angular/router/bundles/router',
            '@angular/forms': '@angular/forms/bundles/forms',
            '@angular/upgrade': '@angular/upgrade/bundles/upgrade',
            '@angular/platform-browser': '@angular/platform-browser/bundles/platform-browser',
            '@angular/platform-browser/animations': '@angular/platform-browser/bundles/platform-browser-animations',
            '@angular/platform-browser-dynamic': '@angular/platform-browser-dynamic/bundles/platform-browser-dynamic',
        };
        for (let packageKey in packages) {
            config.map[packageKey] = `npm:${packages[packageKey]}.umd.js`;
        }
    }
    function addRxjs(config) {
        config.map[`rxjs`] = `npm:rxjs`;
        config.packages[`rxjs`] = {
            main: 'Rx.js',
        };
        // TODO remove after reactivex/rxjs#2971 is closed
        config.packages[`rxjs/operators`] = {
            main: 'index.js',
            defaultExtension: 'js',
        };
    }
    function addAngularTesting(config) {
        let packages = {
            '@angular/core/testing': '@angular/core/bundles/core-testing',
            '@angular/common/testing': '@angular/common/bundles/common-testing',
            '@angular/compiler/testing': '@angular/compiler/bundles/compiler-testing',
            '@angular/platform-browser/testing': '@angular/platform-browser/bundles/platform-browser-testing',
            '@angular/platform-browser-dynamic/testing': '@angular/platform-browser-dynamic/bundles/platform-browser-dynamic-testing',
            '@angular/http/testing': '@angular/http/bundles/http-testing',
        };
        for (let packageKey in packages) {
            config.map[packageKey] = `npm:${packages[packageKey]}.umd.js`;
        }
    }
    function addNgNotifications(config) {
        config.map[`angular2-notifications`] = `npm:angular2-notifications`;
        config.map[`reflect-metadata`] = `npm:reflect-metadata`;
        config.packages[`angular2-notifications`] = {
            main: 'angular2-notifications.umd.js',
            defaultExtension: 'js',
        };
        config.packages[`reflect-metadata`] = {
            main: 'Reflect.js',
        };
    }
    function addNgSlimLoadingBar(config) {
        config.map[`ng2-slim-loading-bar`] = `npm:ng2-slim-loading-bar/bundles/index.umd.js`;
    }
    function addNgNouislider(config) {
        config.map[`nouislider`] = `npm:nouislider`;
        config.packages[`nouislider`] = {
            main: 'distribute/nouislider.js',
            defaultExtension: 'js',
        };
        config.map[`ng2-nouislider`] = `npm:ng2-nouislider`;
        config.packages[`ng2-nouislider`] = {
            main: 'src/nouislider.js',
            defaultExtension: 'js',
        };
    }
    function addFaker(config) {
        config.map[`faker`] = `npm:faker/build/faker`;
    }
})(specConfig || (specConfig = {}));
System.config(specConfig.build());
//# sourceMappingURL=systemjs.conf.spec.js.map