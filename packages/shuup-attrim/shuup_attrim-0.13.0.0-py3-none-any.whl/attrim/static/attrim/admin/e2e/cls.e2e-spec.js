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
const init_1 = require("./utils/init");
const navigation_1 = require("./utils/navigation");
const navigation_2 = require("./utils/navigation");
// TODO waitForAngular
// TODO remove async (its buggy)
describe('cls', () => {
    beforeAll((done) => __awaiter(this, void 0, void 0, function* () {
        yield init_1.init();
        done();
    }));
    it('edits the class name', (done) => __awaiter(this, void 0, void 0, function* () {
        yield navigation_2.loadClsEditForm();
        let clsNameInputEn = protractor_2.$('#cls-name trans-str input[data-lang-code="en"]');
        let clsNameEnOld = yield clsNameInputEn.getAttribute('value');
        let clsNameEnNew = 'new english name';
        yield clsNameInputEn.clear();
        yield clsNameInputEn.sendKeys(clsNameEnNew);
        yield protractor_2.$('#cls-save-button').click();
        yield protractor_1.browser.waitForAngular();
        yield navigation_2.loadClsEditForm();
        let clsNameInputEnUpdated = protractor_2.$('#cls-name trans-str input[data-lang-code="en"]');
        expect(yield clsNameInputEnUpdated.getAttribute('value')).toBe(clsNameEnNew);
        // reset to the old name for the other tests
        yield clsNameInputEn.clear();
        yield clsNameInputEn.sendKeys(clsNameEnOld);
        yield protractor_2.$('#cls-save-button').click();
        yield protractor_1.browser.waitForAngular();
        done();
    }));
    it('creates a cls', () => __awaiter(this, void 0, void 0, function* () {
        yield navigation_1.loadClsNewForm();
        let clsCode = 'cls_code';
        yield protractor_2.$('#cls-code input').sendKeys(clsCode);
        yield protractor_2.$('#cls-name trans-str input[data-lang-code="en"]').sendKeys('en name');
        yield protractor_1.browser.waitForAngularEnabled(false);
        yield protractor_2.$('#cls-create-button').click();
        yield protractor_1.browser.waitForAngular();
        // protractor 5.1.2 throws an error on the direct location set, for now
        // it seems like that crutch is the only option (I've got the solution
        // somewhere on stackoverflow)
        yield protractor_1.browser.sleep(200);
        yield protractor_1.browser.wait(() => __awaiter(this, void 0, void 0, function* () { return yield protractor_2.$('cls-form').isPresent(); }));
        yield protractor_1.browser.waitForAngularEnabled(true);
        yield protractor_1.browser.waitForAngular();
        let clsCodeInputValue = yield protractor_2.$('#cls-code input').getAttribute('value');
        expect(clsCodeInputValue).toBe(clsCode);
    }));
});
//# sourceMappingURL=cls.e2e-spec.js.map