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
const navigation_1 = require("./utils/navigation");
const init_1 = require("./utils/init");
describe('option form', () => {
    beforeAll((done) => __awaiter(this, void 0, void 0, function* () {
        yield init_1.init();
        done();
    }));
    beforeEach((done) => __awaiter(this, void 0, void 0, function* () {
        yield navigation_1.loadClsEditForm();
        done();
    }));
    it('inits the options', () => {
        let optionValueInputEn = protractor_2.$$('option-form trans-str input[data-lang-code="en"]').first();
        let optionValueInputEnValue = optionValueInputEn.getAttribute('value');
        expect(optionValueInputEnValue).toBe('english');
    });
    it('edits the option value (trans str)', (done) => __awaiter(this, void 0, void 0, function* () {
        let optionValueButtonFiSelector = `option-form trans-str .button[data-lang-code="fi"]`;
        yield protractor_2.$$(optionValueButtonFiSelector).first().click();
        let optionValueInputFiSelector = `option-form trans-str input[data-lang-code="fi"]`;
        let optionValueInputFi = protractor_2.$(optionValueInputFiSelector);
        let optionValueInputFiValueNew = 'new fi str';
        yield optionValueInputFi.clear();
        yield optionValueInputFi.sendKeys(optionValueInputFiValueNew);
        yield protractor_2.$('#cls-save-button').click();
        yield protractor_1.browser.waitForAngular();
        yield navigation_1.loadClsEditForm();
        yield protractor_2.$$(optionValueButtonFiSelector).first().click();
        let optionValueInputFiValue = yield protractor_2.$(optionValueInputFiSelector).getAttribute('value');
        expect(optionValueInputFiValue).toBe(optionValueInputFiValueNew);
        done();
    }));
    it('adds and deletes an option', (done) => __awaiter(this, void 0, void 0, function* () {
        // create a new option
        protractor_2.$('#add-option').click();
        let optionNewValue = 'some value';
        let optionInputSelector = `option-form trans-str input[data-lang-code="en"]`;
        let optionNewInput = protractor_2.$$(optionInputSelector).last();
        yield optionNewInput.sendKeys(optionNewValue);
        yield protractor_2.$('#cls-save-button').click();
        yield protractor_1.browser.waitForAngular();
        // check that the option was created
        yield navigation_1.loadClsEditForm();
        let optionNewValueActual = yield optionNewInput.getAttribute('value');
        expect(optionNewValueActual).toBe(optionNewValue);
        // remove the option
        let optionNewRemoveInput = protractor_2.$$('option-form .option-remove input').last();
        yield optionNewRemoveInput.click();
        yield protractor_2.$('#cls-save-button').click();
        yield protractor_1.browser.waitForAngular();
        // check that the option was removed
        yield navigation_1.loadClsEditForm();
        let optionLastInputValue = yield protractor_2.$$(optionInputSelector).last()
            .getAttribute('value');
        expect(optionLastInputValue).not.toBe(optionNewValue);
        done();
    }));
});
//# sourceMappingURL=options.e2e-spec.js.map