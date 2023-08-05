"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
initializeKarma();
function initializeKarma() {
    return __awaiter(this, void 0, void 0, function* () {
        stopKarmaDefaultInit();
        mockDjangoEnv();
        try {
            let loadedModules = yield loadAngularTestModules();
            initAngularTestEnvironment(loadedModules);
            yield loadAngularTestCases();
            __karma__.start();
        }
        catch (error) {
            console.log(error);
            __karma__.error(error);
        }
    });
}
function stopKarmaDefaultInit() {
    __karma__.loaded = () => { };
}
function mockDjangoEnv() {
    let globalMocks = {
        isEditForm: true,
        langCodes: ['en', 'fi', 'fr'],
        defaultLang: 'en',
    };
    window.DJANGO = globalMocks;
}
function loadAngularTestModules() {
    return __awaiter(this, void 0, void 0, function* () {
        //noinspection JSFileReferences
        let modulesUpload = Promise.all([
            System.import('@angular/core/testing'),
            System.import('@angular/platform-browser-dynamic/testing'),
        ]);
        return modulesUpload;
    });
}
function initAngularTestEnvironment(loadedModules) {
    let coreTestingModule = loadedModules[0];
    let platformBrowserModule = loadedModules[1];
    coreTestingModule.TestBed.initTestEnvironment(platformBrowserModule.BrowserDynamicTestingModule, platformBrowserModule.platformBrowserDynamicTesting());
}
function loadAngularTestCases() {
    let testCasePaths = getAngularTestCasePaths();
    let loadingRequests = testCasePaths.map(path => {
        return System.import(path);
    });
    let loadingRequest = Promise.all(loadingRequests);
    return loadingRequest;
}
function getAngularTestCasePaths() {
    let karmaFilePaths = Object.keys(__karma__.files);
    let testCasePaths = karmaFilePaths.filter(path => {
        let isTestCase = /app\/.*spec\.js$/.test(path);
        return isTestCase;
    });
    return testCasePaths;
}
//# sourceMappingURL=karma.shim.js.map