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
const testing_2 = require("@angular/core/testing");
const trans_str_comp_1 = require("app/cls-form/fields/trans-str.comp");
const option_form_comp_1 = require("app/cls-form/fields/option-form.comp");
const type_enum_1 = require("app/type.enum");
const platform_browser_1 = require("@angular/platform-browser");
const notify_service_1 = require("app/services/notify.service");
const angular2_notifications_1 = require("angular2-notifications");
const option_json_service_1 = require("app/services/network/serializers/option-json.service");
const option_service_1 = require("app/services/network/option.service");
const option_model_1 = require("app/models/option.model");
const cookie_service_1 = require("app/services/network/cookie.service");
const csrf_service_1 = require("app/services/network/csrf.service");
const angular2_semantic_ui_1 = require("angular2-semantic-ui");
describe('option tests', () => {
    let self;
    beforeEach(testing_1.async(() => {
        testing_2.TestBed.configureTestingModule({
            imports: [forms_1.FormsModule, angular2_semantic_ui_1.L_SEMANTIC_UI_MODULE],
            declarations: [option_form_comp_1.OptionFormComponent, trans_str_comp_1.TransStrComponent],
            providers: [
                notify_service_1.NotifyService, angular2_notifications_1.NotificationsService, option_json_service_1.OptionJsonSerializerService,
                cookie_service_1.CookieService, csrf_service_1.CsrfService,
                { provide: option_service_1.OptionNetworkService, useValue: new OptionNetworkServiceStub() },
            ],
        });
        testing_2.TestBed.compileComponents();
    }));
    beforeEach(() => {
        let fixture = testing_2.TestBed.createComponent(option_form_comp_1.OptionFormComponent);
        self = {
            fixture: fixture,
            debugElem: fixture.debugElement,
            component: fixture.componentInstance,
        };
    });
    it('syncs the input and value with Type.TRANS_STR', () => {
        self.component.initForm({ type: type_enum_1.Type.TRANS_STR });
        let input = self.fixture.debugElement.query(platform_browser_1.By.css('input'));
        let newValue = 'new value';
        input.nativeElement.value = newValue;
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        let filledButton = self.debugElem.query(platform_browser_1.By.css('.checkmark.box'));
        expect(filledButton).not.toBeNull();
        expect(self.component.model.value[window.DJANGO.defaultLang]).toBe(newValue);
    });
    it('syncs the input and value with Type.STR', () => {
        self.component.initForm({ type: type_enum_1.Type.STR });
        let input = self.fixture.debugElement.query(platform_browser_1.By.css('input'));
        let newValue = 'new value';
        input.nativeElement.value = newValue;
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        expect(self.component.model.value).toBe(newValue);
    });
    it('syncs the input and value with Type.INT', () => {
        self.component.initForm({ type: type_enum_1.Type.INT });
        let input = self.fixture.debugElement.query(platform_browser_1.By.css('input'));
        let newValue = '5';
        input.nativeElement.value = newValue;
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        let component = self.component;
        expect(component.model.value.toString()).toBe(newValue);
    });
    it('syncs the input and value with Type.DECIMAL', () => {
        self.component.initForm({ type: type_enum_1.Type.DECIMAL });
        let input = self.fixture.debugElement.query(platform_browser_1.By.css('input'));
        let newValue = '5.5';
        input.nativeElement.value = newValue;
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        expect(self.component.model.value.toString()).toBe(newValue);
    });
});
class OptionNetworkServiceStub {
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            return new option_model_1.Option({
                pk: pk,
                clsPk: 1,
                type: type_enum_1.Type.TRANS_STR,
                isSaved: true,
            });
        });
    }
    save(option) {
        return __awaiter(this, void 0, void 0, function* () {
            return {};
        });
    }
}
//# sourceMappingURL=option-form.comp.spec.js.map