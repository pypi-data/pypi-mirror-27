exports.config = {
    framework: 'jasmine',
    capabilities: {
        browserName: 'chrome',
        chromeOptions: {
            'args': ['--no-sandbox', '--user-data-dir=./.browsers/chrome_protractor'],
        },
    },
    specs: [
        './e2e/cls.e2e-spec.js',
        './e2e/options.e2e-spec.js',
    ],
    seleniumServerJar: './node_modules/selenium-server-standalone-jar/jar/selenium-server-standalone-3.7.1.jar',
}
