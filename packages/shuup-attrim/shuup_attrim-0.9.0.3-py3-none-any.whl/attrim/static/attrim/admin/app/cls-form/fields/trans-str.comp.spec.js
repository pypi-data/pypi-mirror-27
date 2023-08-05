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
const forms_1 = require("@angular/forms");
const testing_1 = require("@angular/core/testing");
const platform_browser_1 = require("@angular/platform-browser");
const testing_2 = require("@angular/core/testing");
const trans_str_comp_1 = require("app/cls-form/fields/trans-str.comp");
describe('trans str tests', () => {
    let self;
    beforeEach(testing_1.async(() => {
        testing_2.TestBed.configureTestingModule({
            imports: [forms_1.FormsModule],
            declarations: [trans_str_comp_1.TransStrComponent],
        });
        testing_2.TestBed.compileComponents();
    }));
    beforeEach(() => {
        let fixture = testing_2.TestBed.createComponent(trans_str_comp_1.TransStrComponent);
        self = {
            fixture: fixture,
            debugElem: fixture.debugElement,
            defaultLang: window.DJANGO.defaultLang,
            langCodes: window.DJANGO.langCodes,
        };
        self.fixture.detectChanges();
    });
    it('updates the buttons statuses on input change', () => {
        let root = self.fixture.debugElement;
        let input = root.query(platform_browser_1.By.css('input'));
        input.nativeElement.value = 'new value';
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        let filledIconClasses = '.checkmark.box';
        let filledButton = self.debugElem.query(platform_browser_1.By.css(filledIconClasses));
        expect(filledButton).not.toBeNull();
    });
    it('dynamically displays the active lang code input', testing_1.async(() => __awaiter(this, void 0, void 0, function* () {
        expect(self.defaultLang).toBe(self.langCodes[0]);
        let input0 = yield selectLangInputByLangCodeIndex(0);
        let input0ValueNew = 'input 0 value new';
        setInputValue(input0, input0ValueNew);
        expect(input0.nativeElement.value).toBe(input0ValueNew);
        let input1 = yield selectLangInputByLangCodeIndex(1);
        expect(input1.nativeElement.value).toBe('');
        input0 = yield selectLangInputByLangCodeIndex(0);
        expect(input0.nativeElement.value).toBe(input0ValueNew);
        input1 = yield selectLangInputByLangCodeIndex(1);
        expect(input1.nativeElement.value).toBe('');
        let input1ValueNew = 'input 1 value new';
        setInputValue(input1, input1ValueNew);
        expect(input1.nativeElement.value).toBe(input1ValueNew);
        input0 = yield selectLangInputByLangCodeIndex(0);
        expect(input0.nativeElement.value).toBe(input0ValueNew);
    })));
    function selectLangInputByLangCodeIndex(langIndex) {
        return __awaiter(this, void 0, void 0, function* () {
            let selectLangButton = self.debugElem.query(platform_browser_1.By.css(`.select-lang-button[data-lang-code='${self.langCodes[langIndex]}']`));
            selectLangButton.triggerEventHandler('click', null);
            self.fixture.detectChanges();
            // otherwise it fails to sync the input with respect to the selected
            // lang code
            yield self.fixture.whenStable();
            let input = self.debugElem.query(platform_browser_1.By.css(`input[data-lang-code='${self.langCodes[langIndex]}']`));
            return input;
        });
    }
    function setInputValue(input, value) {
        input.nativeElement.value = value;
        input.nativeElement.dispatchEvent(new Event('input'));
    }
});
//# sourceMappingURL=trans-str.comp.spec.js.map