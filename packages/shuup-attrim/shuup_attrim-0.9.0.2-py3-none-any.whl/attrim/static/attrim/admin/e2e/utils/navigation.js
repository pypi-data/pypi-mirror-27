"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
const protractor_2 = require("protractor");
const protractor_3 = require("protractor");
const protractor_4 = require("protractor");
const django_1 = require("./django");
function login() {
    return __awaiter(this, void 0, void 0, function* () {
        yield protractor_4.browser.waitForAngularEnabled(false);
        let loginPageUrl = `${django_1.DJANGO.url}/sa/login/`;
        yield protractor_4.browser.driver.get(loginPageUrl);
        let usernameField = protractor_3.$('#id_username');
        yield usernameField.sendKeys(django_1.DJANGO.user.username);
        let passwordField = protractor_3.$('#id_password');
        yield passwordField.sendKeys(django_1.DJANGO.user.password);
        let submitButton = protractor_3.$(`button[type="submit"]`);
        yield submitButton.click();
        yield protractor_4.browser.waitForAngularEnabled(true);
    });
}
exports.login = login;
function loadClsEditForm(clsCode = 'language') {
    return __awaiter(this, void 0, void 0, function* () {
        yield protractor_4.browser.waitForAngularEnabled(false);
        yield protractor_4.browser.driver.get(`${django_1.DJANGO.url}/sa/attrim/`);
        let clsLink = protractor_1.element(protractor_2.by.cssContainingText('#picotable tbody a', clsCode));
        yield protractor_4.browser.wait(() => __awaiter(this, void 0, void 0, function* () { return yield clsLink.isPresent(); }));
        yield clsLink.click();
        yield protractor_4.browser.wait(() => __awaiter(this, void 0, void 0, function* () { return protractor_3.$('cls-form').isPresent(); }));
        yield protractor_4.browser.waitForAngularEnabled(true);
        yield protractor_4.browser.waitForAngular();
    });
}
exports.loadClsEditForm = loadClsEditForm;
function loadClsNewForm() {
    return __awaiter(this, void 0, void 0, function* () {
        yield protractor_4.browser.waitForAngularEnabled(false);
        yield protractor_4.browser.driver.get(`${django_1.DJANGO.url}/sa/attrim/new/`);
        yield protractor_4.browser.wait(() => __awaiter(this, void 0, void 0, function* () { return protractor_3.$('cls-form').isPresent(); }));
        yield protractor_4.browser.waitForAngularEnabled(true);
        yield protractor_4.browser.waitForAngular();
    });
}
exports.loadClsNewForm = loadClsNewForm;
//# sourceMappingURL=navigation.js.map