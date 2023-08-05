declare var System: any


System.config(buildConfig())


function buildConfig(): Config {
    let config = {
        baseURL: '/static/attrim/admin',
        paths: {
            'npm:': 'node_modules/'
        },
        map: { },
        packages: {
            '.': {
                defaultJSExtensions: 'js'
            },
            'app': {
                defaultExtension: 'js',
            },
        },
    }
    addAngularCore(config)
    addAngularTesting(config)
    addRxjs(config)
    addNgNotifications(config)
    addNgSemanticUi(config)
    addNgSlimLoadingBar(config)
    return config
}

function addAngularCore(config: Config) {
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
    }
    for (let packageKey in packages) {
        config.map[packageKey] = `npm:${packages[packageKey]}.umd.js`
    }
}

function addRxjs(config: Config) {
    config.map[`rxjs`] = `npm:rxjs`
    config.packages[`rxjs`] = {
        main: 'Rx.js',
    }
}

function addAngularTesting(config: Config) {
    let packages = {
        '@angular/core/testing': '@angular/core/bundles/core-testing',
        '@angular/common/testing': '@angular/common/bundles/common-testing',
        '@angular/compiler/testing': '@angular/compiler/bundles/compiler-testing',
        '@angular/platform-browser/testing': '@angular/platform-browser/bundles/platform-browser-testing',
        '@angular/platform-browser-dynamic/testing': '@angular/platform-browser-dynamic/bundles/platform-browser-dynamic-testing',
        '@angular/http/testing': '@angular/http/bundles/http-testing',
    }
    for (let packageKey in packages) {
        config.map[packageKey] = `npm:${packages[packageKey]}.umd.js`
    }
}

function addNgSemanticUi(config: Config) {
    let packages = [
        'angular2-semantic-ui',
        'angular2-semantic-ui/components/checkbox',
        'angular2-semantic-ui/components/dimmer',
        'angular2-semantic-ui/components/dropdown',
        'angular2-semantic-ui/components/loader',
        'angular2-semantic-ui/components/modal',
        'angular2-semantic-ui/components/progress',
        'angular2-semantic-ui/components/tab',
        'angular2-semantic-ui/components/accordion',
        'angular2-semantic-ui/components/accordion_panel',
        'angular2-semantic-ui/components/popup',
        'angular2-semantic-ui/components/pagination',
        'angular2-semantic-ui/components/tags-input',
        'angular2-semantic-ui/components/rating',
    ]
    for (let packagePath of packages) {
        config.map[packagePath] = `npm:${packagePath}`
        config.packages[packagePath] = {
            main: './index.js',
            defaultExtension: 'js',
        }
    }
}

function addNgNotifications(config: Config) {
    config.map[`angular2-notifications`] = `npm:angular2-notifications`
    config.map[`reflect-metadata`] = `npm:reflect-metadata`
    config.packages[`angular2-notifications`] = {
        main: 'dist/index.js',
        defaultExtension: 'js',
    }
    config.packages[`reflect-metadata`] = {
        main: 'Reflect.js',
    }
}

function addNgSlimLoadingBar(config: Config) {
    config.map[`ng2-slim-loading-bar`] = `npm:ng2-slim-loading-bar/bundles/index.umd.js`
}

type Config = any
