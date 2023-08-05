"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
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
const cls_form_comp_1 = require("app/cls-form/cls-form.comp");
const option_form_comp_1 = require("app/cls-form/fields/option-form.comp");
const trans_str_comp_1 = require("app/cls-form/fields/trans-str.comp");
const core_1 = require("@angular/core");
const option_model_1 = require("app/models/option.model");
const cls_model_1 = require("app/models/cls.model");
const type_enum_1 = require("app/type.enum");
const cls_service_1 = require("app/services/network/cls.service");
const iter_enum_pipe_1 = require("app/iter-enum.pipe");
const cls_json_service_1 = require("app/services/network/serializers/cls-json.service");
const product_type_service_1 = require("app/services/network/product-type.service");
const product_type_model_1 = require("app/models/product-type.model");
const notify_service_1 = require("app/services/notify.service");
const angular2_notifications_1 = require("angular2-notifications");
const ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
const option_json_service_1 = require("app/services/network/serializers/option-json.service");
const option_service_1 = require("app/services/network/option.service");
const product_type_json_service_1 = require("app/services/network/serializers/product-type-json.service");
const http_1 = require("@angular/http");
const cookie_service_1 = require("app/services/network/cookie.service");
const csrf_service_1 = require("app/services/network/csrf.service");
const angular2_notifications_2 = require("angular2-notifications");
const angular2_semantic_ui_1 = require("angular2-semantic-ui");
describe('cls form tests', () => {
    let self;
    beforeEach(testing_1.async(() => {
        testing_2.TestBed.configureTestingModule({
            imports: [FakeModule],
        });
        testing_2.TestBed.compileComponents();
    }));
    beforeEach(() => {
        initTestCase();
        resetTypeInput();
    });
    it('can handle name update', () => {
        let clsNameSection = self.debugElem.query(platform_browser_1.By.css('#cls-name'));
        let input = clsNameSection.query(platform_browser_1.By.css('input'));
        input.nativeElement.value = 'new value';
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        let updatedButtonClass = '.checkmark.box';
        let updatedButton = clsNameSection.query(platform_browser_1.By.css(updatedButtonClass));
        expect(updatedButton).not.toBeNull();
    });
    it('can handle product type update', (done) => __awaiter(this, void 0, void 0, function* () {
        // wait for the fake network request
        yield self.fixture.whenStable();
        self.component.productTypeList = [
            new product_type_model_1.ProductType(1, 'test name 1'),
            new product_type_model_1.ProductType(2, 'test name 2'),
        ];
        self.fixture.detectChanges();
        let productTypeToSelect = self.component.productTypeList[1];
        expect(self.component.model.productType).not.toBe(productTypeToSelect);
        let productTypeSelectInput = self.debugElem.query(platform_browser_1.By.css('#cls-product-type select'));
        productTypeSelectInput.nativeElement.value = productTypeToSelect.pk;
        productTypeSelectInput.nativeElement.dispatchEvent(new Event('change'));
        expect(self.component.model.productType).toBe(productTypeToSelect);
        done();
    }));
    it('updates the option-form trans-str buttons status an on input change', () => {
        self.component.addOption();
        self.component.addOption();
        let input = self.debugElem.query(platform_browser_1.By.css('option-form trans-str input'));
        input.nativeElement.value = 'new value';
        input.nativeElement.dispatchEvent(new Event('input'));
        self.fixture.detectChanges();
        let updatedButtonClass = '.checkmark.box';
        let updatedButton = self.debugElem.query(platform_browser_1.By.css(updatedButtonClass));
        expect(updatedButton).not.toBeNull();
    });
    function initTestCase() {
        let fixture = testing_2.TestBed.createComponent(cls_form_comp_1.ClsFormComponent);
        self = {
            fixture: fixture,
            component: fixture.componentInstance,
            debugElem: fixture.debugElement,
        };
        self.fixture.detectChanges();
    }
    function resetTypeInput() {
        let selectInput = self.debugElem.query(platform_browser_1.By.css('#cls-type select'));
        selectInput.nativeElement.value = type_enum_1.Type.TRANS_STR;
        selectInput.nativeElement.dispatchEvent(new Event('change'));
    }
});
class ClsNetworkServiceStub {
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let cls = new cls_model_1.Cls({
                code: 'test mock',
                type: type_enum_1.Type.TRANS_STR,
                name: {
                    en: 'english name',
                    fi: 'not en name',
                },
                productType: { name: 'test', pk: 1 },
            });
            return cls;
        });
    }
}
class ProductTypeNetworkServiceStub {
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            return { name: 'Mock product type', pk: 1 };
        });
    }
    //noinspection JSUnusedGlobalSymbols
    getAll() {
        return __awaiter(this, void 0, void 0, function* () {
            return [{ name: 'Mock product type', pk: 1 }];
        });
    }
}
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
/**
 * The `configureTestingModule` method does not support `entryComponents` in
 * angular 4.0.3, so they must be included through a fake module.
 */
let FakeModule = class FakeModule {
};
FakeModule = __decorate([
    core_1.NgModule({
        imports: [
            platform_browser_1.BrowserModule, forms_1.FormsModule, http_1.HttpModule, ng2_slim_loading_bar_1.SlimLoadingBarModule.forRoot(),
            angular2_notifications_2.SimpleNotificationsModule.forRoot(), angular2_semantic_ui_1.L_SEMANTIC_UI_MODULE,
        ],
        declarations: [cls_form_comp_1.ClsFormComponent, option_form_comp_1.OptionFormComponent, trans_str_comp_1.TransStrComponent, iter_enum_pipe_1.IterateEnumPipe],
        entryComponents: [option_form_comp_1.OptionFormComponent],
        exports: [iter_enum_pipe_1.IterateEnumPipe],
        providers: [
            cls_service_1.ClsNetworkService, cls_json_service_1.ClsJsonSerializerService,
            product_type_service_1.ProductTypeNetworkService, notify_service_1.NotifyService, angular2_notifications_1.NotificationsService,
            option_json_service_1.OptionJsonSerializerService, csrf_service_1.CsrfService,
            product_type_json_service_1.ProductTypeJsonSerializerService, cookie_service_1.CookieService,
            { provide: option_service_1.OptionNetworkService, useValue: new OptionNetworkServiceStub() },
            { provide: cls_service_1.ClsNetworkService, useValue: new ClsNetworkServiceStub() },
            { provide: product_type_service_1.ProductTypeNetworkService, useValue: new ProductTypeNetworkServiceStub() },
        ],
    })
], FakeModule);
//# sourceMappingURL=cls-form.comp.spec.js.map