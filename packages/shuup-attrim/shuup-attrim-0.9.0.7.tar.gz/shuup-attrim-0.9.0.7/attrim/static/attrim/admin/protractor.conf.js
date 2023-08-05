exports.config = {
    framework: 'jasmine',
    capabilities: {
        browserName: 'chrome',
        chromeOptions: {
            'args': ['--user-data-dir=./.browsers/chrome_protractor'],
        },
    },
    specs: [
        './e2e/cls.e2e-spec.js',
        './e2e/options.e2e-spec.js',
    ],
    seleniumServerJar: './node_modules/selenium-server-standalone-jar/jar/selenium-server-standalone-3.5.0.jar',
}
