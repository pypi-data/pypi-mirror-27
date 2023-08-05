DEFAULT_TIMEOUT_INTERVAL = 9999999999999
Error.stackTraceLimit = Infinity


module.exports = function(config) {
    config.set({
        basePath: '.',
        
        frameworks: ['jasmine'],
        
        files: [
            'node_modules/semantic-ui-css/semantic.min.css',
            // systemjs for module loading
            'node_modules/systemjs/dist/system.src.js',

            'node_modules/core-js/client/shim.js',
            
            // zone.js dependencies
            'node_modules/zone.js/dist/zone.js',
            'node_modules/zone.js/dist/long-stack-trace-zone.js',
            'node_modules/zone.js/dist/proxy.js',
            'node_modules/zone.js/dist/sync-test.js',
            'node_modules/zone.js/dist/jasmine-patch.js',
            'node_modules/zone.js/dist/async-test.js',
            'node_modules/zone.js/dist/fake-async-test.js',

            'systemjs.conf.spec.js',
            'karma.shim.js',
            {pattern: 'systemjs.conf.spec.js.map', included: false, watched: true},
            {pattern: 'karma.shim.js.map', included: false, watched: true},

            // paths loaded via module imports

            {pattern: 'node_modules/rxjs/**/*.js', included: false, watched: false},
            {pattern: 'node_modules/rxjs/**/*.js.map', included: false, watched: false},

            // angular itself
            {pattern: 'node_modules/@angular/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/@angular/**/*.js.map', included: false, watched: true},

            // ng2-slim-loading-bar
            {pattern: 'node_modules/ng2-slim-loading-bar/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/ng2-slim-loading-bar/**/*.js.map', included: false, watched: true},

            // angular2-notifications
            {pattern: 'node_modules/angular2-notifications/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/angular2-notifications/**/*.js.map', included: false, watched: true},

            // angular2-semantic-ui
            {pattern: 'node_modules/angular2-semantic-ui/**/*.js', included: false, watched: true},
            {pattern: 'node_modules/angular2-semantic-ui/**/*.js.map', included: false, watched: true},

            {pattern: 'app/**/*.js', included: false, watched: true},
            {pattern: 'app/**/*.ts', included: false, watched: false},
            {pattern: 'app/**/*.js.map', included: false, watched: false},
            {pattern: 'app/**/*.html', included: false, watched: true},
            {pattern: 'app/**/*.css', included: false, watched: true},
        ],

        exclude: [
            'e2e/**/*',
            'e2e/**/*',
            // or @angular/compiler-cli will break the tests
            'node_modules/**/*spec.js',
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
                flags: ['--user-data-dir=./.browsers/chrome_karma'],
            },
        },
        singleRun: true,
   })
}
