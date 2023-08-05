declare var System: any
declare var __karma__: any


initializeKarma()


async function initializeKarma() {
    stopKarmaDefaultInit()
    mockDjangoEnv()

    try {
        let loadedModules: [any, any] = await loadAngularTestModules()
        initAngularTestEnvironment(loadedModules)
        await loadAngularTestCases()
        __karma__.start()
    } catch (error) {
        console.log(error)
        __karma__.error(error)
    }
}


function stopKarmaDefaultInit() {
    __karma__.loaded = () => {}
}


function mockDjangoEnv() {
    let globalMocks: DjangoProvidedGlobals = {
        isEditForm: true,
        langCodes: ['en', 'fi', 'fr'],
        defaultLang: 'en',
    }
    window.DJANGO = globalMocks
}


async function loadAngularTestModules(): Promise<[any, any]> {
    //noinspection JSFileReferences
    let modulesUpload = Promise.all([
        System.import('@angular/core/testing'),
        System.import('@angular/platform-browser-dynamic/testing'),
    ])
    return modulesUpload
}


function initAngularTestEnvironment(loadedModules: [any, any]) {
    let coreTestingModule = loadedModules[0]
    let platformBrowserModule = loadedModules[1]

    coreTestingModule.TestBed.initTestEnvironment(
        platformBrowserModule.BrowserDynamicTestingModule,
        platformBrowserModule.platformBrowserDynamicTesting(),
    )
}


function loadAngularTestCases(): Promise<any> {
    let testCasePaths = getAngularTestCasePaths()
    let loadingRequests: Promise<any>[] = testCasePaths.map(path => {
        return System.import(path)
    })
    let loadingRequest = Promise.all(loadingRequests)
    return loadingRequest
}


function getAngularTestCasePaths(): Array<string> {
    let karmaFilePaths: Array<string> = Object.keys(__karma__.files)
    let testCasePaths: Array<string> = karmaFilePaths.filter(path => {
        let isTestCase: boolean = /app\/.*spec\.js$/.test(path)
        return isTestCase
    })
    return testCasePaths
}
