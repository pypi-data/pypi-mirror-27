webpackJsonp([1],{

/***/ 1083:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
__webpack_require__(167);
__webpack_require__(355);
const platform_browser_dynamic_1 = __webpack_require__(254);
const app_module_1 = __webpack_require__(1084);
const core_1 = __webpack_require__(1);
core_1.enableProdMode();
// noinspection JSIgnoredPromiseFromCall
platform_browser_dynamic_1.platformBrowserDynamic().bootstrapModule(app_module_1.AppModule);


/***/ }),

/***/ 1084:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
const platform_browser_1 = __webpack_require__(50);
const app_comp_1 = __webpack_require__(1085);
const trans_str_comp_1 = __webpack_require__(1086);
const forms_1 = __webpack_require__(45);
const ng2_slim_loading_bar_1 = __webpack_require__(175);
const cls_form_comp_1 = __webpack_require__(1089);
const option_form_comp_1 = __webpack_require__(446);
const iter_enum_pipe_1 = __webpack_require__(1096);
const cls_service_1 = __webpack_require__(208);
const cls_json_service_1 = __webpack_require__(451);
const angular2_notifications_1 = __webpack_require__(123);
const notify_service_1 = __webpack_require__(455);
const product_type_service_1 = __webpack_require__(209);
const option_json_service_1 = __webpack_require__(450);
const option_service_1 = __webpack_require__(449);
const product_type_json_service_1 = __webpack_require__(453);
const cookie_service_1 = __webpack_require__(454);
const csrf_service_1 = __webpack_require__(210);
const animations_1 = __webpack_require__(253);
const angular2_notifications_2 = __webpack_require__(123);
const ng2_semantic_ui_1 = __webpack_require__(358);
const http_1 = __webpack_require__(72);
let AppModule = class AppModule {
};
AppModule = __decorate([
    core_1.NgModule({
        imports: [
            platform_browser_1.BrowserModule, forms_1.FormsModule, http_1.HttpClientModule, animations_1.BrowserAnimationsModule,
            ng2_slim_loading_bar_1.SlimLoadingBarModule.forRoot(), angular2_notifications_2.SimpleNotificationsModule.forRoot(),
            ng2_semantic_ui_1.SuiModule,
        ],
        declarations: [
            app_comp_1.AppComponent, cls_form_comp_1.ClsFormComponent, option_form_comp_1.OptionFormComponent, trans_str_comp_1.TransStrComponent,
            iter_enum_pipe_1.IterateEnumPipe,
        ],
        entryComponents: [option_form_comp_1.OptionFormComponent],
        exports: [iter_enum_pipe_1.IterateEnumPipe],
        providers: [
            cls_service_1.ClsNetworkService, cls_json_service_1.ClsJsonSerializerService,
            product_type_service_1.ProductTypeNetworkService, notify_service_1.NotifyService, angular2_notifications_1.NotificationsService,
            option_json_service_1.OptionJsonSerializerService, option_service_1.OptionNetworkService,
            product_type_json_service_1.ProductTypeJsonSerializerService, cookie_service_1.CookieService, csrf_service_1.CsrfService,
        ],
        bootstrap: [app_comp_1.AppComponent],
    })
], AppModule);
exports.AppModule = AppModule;


/***/ }),

/***/ 1085:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
let AppComponent = class AppComponent {
};
AppComponent = __decorate([
    core_1.Component({
        selector: 'app',
        template: `<cls-form></cls-form>`,
    })
], AppComponent);
exports.AppComponent = AppComponent;


/***/ }),

/***/ 1086:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
const core_2 = __webpack_require__(1);
const core_3 = __webpack_require__(1);
const core_4 = __webpack_require__(1);
const core_5 = __webpack_require__(1);
let TransStrComponent = class TransStrComponent {
    constructor() {
        // must reflect the pattern `{orig_name}Change` for the `[(ngModel)]` binding
        this.translationsChange = new core_4.EventEmitter();
        // noinspection JSMismatchedCollectionQueryUpdate
        this.langCodes = window.DJANGO.langCodes;
        this.langCodeSelected = window.DJANGO.defaultLang;
    }
    ngOnInit() {
        this.initTranslation();
    }
    // noinspection JSUnusedLocalSymbols
    selectLangCode(langCode) {
        this.langCodeSelected = langCode;
    }
    setButtonClasses(langCode) {
        let isEmpty = this.isTranslationEmpty(langCode);
        if (isEmpty) {
            let unfilledIcon = { square: true, outline: true, icon: true };
            return unfilledIcon;
        }
        else {
            let filledIcon = { checkmark: true, box: true, icon: true };
            return filledIcon;
        }
    }
    updateTranslations(langCode, value) {
        this.translations[langCode] = value;
        this.translationsChange.emit(this.translations);
    }
    initTranslation() {
        if (this.translations === undefined) {
            this.translations = {};
        }
        for (let langCode of window.DJANGO.langCodes) {
            this.translations[langCode] = '';
        }
    }
    isTranslationEmpty(langCode) {
        let transCurrent = this.translations[langCode];
        let isEmpty = transCurrent === '' || transCurrent === undefined;
        let isNotDefaultTrans = langCode !== window.DJANGO.defaultLang;
        let isMirroringDefaultTrans = (transCurrent === this.translations[window.DJANGO.defaultLang]);
        return isEmpty || (isNotDefaultTrans && isMirroringDefaultTrans);
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", Object)
], TransStrComponent.prototype, "translations", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", Object)
], TransStrComponent.prototype, "translationsChange", void 0);
TransStrComponent = __decorate([
    core_1.Component({
        selector: 'trans-str',
        template: __webpack_require__(1087),
        styles: [__webpack_require__(1088)],
        // the encapsulation is screwed up for dynamic components in 4.0.3
        encapsulation: core_5.ViewEncapsulation.None,
    })
], TransStrComponent);
exports.TransStrComponent = TransStrComponent;


/***/ }),

/***/ 1087:
/***/ (function(module, exports) {

module.exports = "<section class=\"fields\"><div class=\"field\" id=\"inputs\"><div class=\"lang-input field\" *ngFor=\"let langCode of langCodes\"><input type=\"text\" *ngIf=\"langCodeSelected === langCode\" [(ngModel)]=\"translations[langCode]\" (keyup)=\"updateTranslations(langCode, $event.target.value)\" [attr.data-lang-code]=\"langCode\"/></div></div><div class=\"field select-lang\"><div class=\"ui basic buttons\"><div class=\"select-lang-button ui button\" *ngFor=\"let langCode of langCodes\" (click)=\"selectLangCode(langCode)\" [class.active]=\"langCodeSelected === langCode\" [attr.data-lang-code]=\"langCode\"><i [ngClass]=\"setButtonClasses(langCode)\"></i>{{ langCode }}</div></div></div></section>";

/***/ }),

/***/ 1088:
/***/ (function(module, exports) {

module.exports = "trans-str .select-lang {\n  display: flex;\n  align-self: flex-end; }\n"

/***/ }),

/***/ 1089:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const type_enum_1 = __webpack_require__(129);
const option_form_comp_1 = __webpack_require__(446);
const core_2 = __webpack_require__(1);
const core_3 = __webpack_require__(1);
const core_4 = __webpack_require__(1);
const type_enum_decorator_1 = __webpack_require__(447);
const core_5 = __webpack_require__(1);
const cls_model_1 = __webpack_require__(452);
const cls_service_1 = __webpack_require__(208);
const product_type_service_1 = __webpack_require__(209);
const notify_service_1 = __webpack_require__(455);
const ng2_slim_loading_bar_1 = __webpack_require__(175);
const async_show_loading_bar_decorator_1 = __webpack_require__(1092);
const async_with_notify_decorator_1 = __webpack_require__(1093);
// TODO refactor: move options out into some kind of `options-form.comp`
let ClsFormComponent = class ClsFormComponent {
    constructor(loadingBarService, notifyService, networkService, productTypeService, componentFactoryResolver) {
        this.loadingBarService = loadingBarService;
        this.notifyService = notifyService;
        this.networkService = networkService;
        this.productTypeService = productTypeService;
        this.componentFactoryResolver = componentFactoryResolver;
        this.model = new cls_model_1.Cls({ code: '', type: type_enum_1.Type.INT, productType: { name: '', pk: 0 } });
        this.optionCompRefSet = new Set();
    }
    ngOnInit() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.initForm();
        });
    }
    addOption(args) {
        let optionCompRef = this.createOptionComponent();
        if (args) {
            // noinspection JSIgnoredPromiseFromCall
            optionCompRef.instance.initForm(args);
        }
        else {
            // noinspection JSIgnoredPromiseFromCall
            optionCompRef.instance.initForm({ type: this.model.type, clsPk: this.model.pk });
        }
        this.optionCompRefSet.add(optionCompRef);
    }
    /**
     * Don't use the loading bar here because protractor [5.1|5.2] hangs on it with a
     * probability of ~15%.
     */
    // @asyncShowLoadingBar
    save() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsSaved = yield this.saveCls();
            yield this.saveOptions(clsSaved.pk);
        });
    }
    create() {
        return __awaiter(this, void 0, void 0, function* () {
            this.fillInModelWithDefaultValues(this.model);
            let clsCreated = yield this.networkService.create(this.model);
            yield this.saveOptions(clsCreated.pk);
            location.assign(`/sa/attrim/${clsCreated.pk}/`);
        });
    }
    selectTypeOptionFormatter(optionValue) {
        switch (optionValue) {
            case type_enum_1.Type.INT:
                return 'integer';
            case type_enum_1.Type.DECIMAL:
                return 'decimal';
            case type_enum_1.Type.STR:
                return 'string';
            case type_enum_1.Type.TRANS_STR:
                return 'translated string';
            default:
                throw new Error('The type is not supported.');
        }
    }
    selectProductTypeOptionFormatter(optionValue) {
        return optionValue.name;
    }
    saveCls() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsSaved = yield this.networkService.save(this.model);
            this.model = clsSaved;
            let productType = this.productTypeList.find(type => type.pk === clsSaved.productType.pk);
            this.model.productType = productType;
            return clsSaved;
        });
    }
    saveOptions(clsPk) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionSavePromises = [];
            for (let optionCompRef of this.optionCompRefSet) {
                optionCompRef.instance.model.clsPk = clsPk;
                let savePromise = optionCompRef.instance.save();
                optionSavePromises.push(savePromise);
            }
            yield Promise.all(optionSavePromises);
        });
    }
    initForm() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.initProductTypeList();
            if (window.DJANGO.isEditForm) {
                yield this.loadFormDataFromServer();
            }
            else {
                this.loadFormDataDefault();
            }
        });
    }
    initProductTypeList() {
        return __awaiter(this, void 0, void 0, function* () {
            this.productTypeList = yield this.productTypeService.getAll();
        });
    }
    loadFormDataFromServer() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsPkToEdit = window.DJANGO.clsPrimaryKey;
            let clsToEdit = yield this.networkService.get(clsPkToEdit);
            this.model = clsToEdit;
            let productType = this.productTypeList.find(type => type.pk === clsToEdit.productType.pk);
            this.model.productType = productType;
            for (let optionPk of clsToEdit.optionsPk) {
                this.addOption({ optionPk: optionPk });
            }
        });
    }
    loadFormDataDefault() {
        let clsDefault = new cls_model_1.Cls({
            code: '',
            type: type_enum_1.Type.INT,
            productType: this.productTypeList[0],
        });
        this.model = clsDefault;
    }
    createOptionComponent() {
        let factory = this.componentFactoryResolver
            .resolveComponentFactory(option_form_comp_1.OptionFormComponent);
        return this.optionsContainerRef.createComponent(factory);
    }
    fillInModelWithDefaultValues(model) {
        let langDefault = window.DJANGO.defaultLang;
        let isNameFilled = (model.name[langDefault] === '') ||
            (model.name[langDefault] === undefined);
        if (isNameFilled) {
            model.name[langDefault] = model.code;
        }
    }
};
__decorate([
    core_4.ViewChild('options', { read: core_3.ViewContainerRef }),
    __metadata("design:type", core_3.ViewContainerRef)
], ClsFormComponent.prototype, "optionsContainerRef", void 0);
__decorate([
    async_with_notify_decorator_1.asyncWithNotify({ onSuccessMsg: 'The saving complete', onErrorMsg: 'The saving failed' }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ClsFormComponent.prototype, "save", null);
__decorate([
    async_show_loading_bar_decorator_1.asyncShowLoadingBar,
    async_with_notify_decorator_1.asyncWithNotify({ onErrorMsg: 'Creation failed' }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ClsFormComponent.prototype, "create", null);
__decorate([
    async_show_loading_bar_decorator_1.asyncShowLoadingBar,
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ClsFormComponent.prototype, "initForm", null);
__decorate([
    async_with_notify_decorator_1.asyncWithNotify({ onErrorMsg: 'Network error during product types retrieving' }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ClsFormComponent.prototype, "initProductTypeList", null);
ClsFormComponent = __decorate([
    core_1.Component({
        selector: 'cls-form',
        template: __webpack_require__(1094),
        styles: [__webpack_require__(1095)],
        encapsulation: core_5.ViewEncapsulation.None,
    }),
    type_enum_decorator_1.TypeEnumDecorator,
    __metadata("design:paramtypes", [ng2_slim_loading_bar_1.SlimLoadingBarService,
        notify_service_1.NotifyService,
        cls_service_1.ClsNetworkService,
        product_type_service_1.ProductTypeNetworkService,
        core_2.ComponentFactoryResolver])
], ClsFormComponent);
exports.ClsFormComponent = ClsFormComponent;


/***/ }),

/***/ 1090:
/***/ (function(module, exports) {

module.exports = "<section class=\"fields\" [class.marked-as-removed]=\"model.isMarkedAsRemoved\"><div class=\"field\" [ngSwitch]=\"model.type\"><label>Value</label><div *ngSwitchCase=\"Type.INT\"><!-- TODO is the `.field` required? why it isn't everywhere else? I remember a css bug?--><div class=\"field\"><input class=\"option-value-int-input\" type=\"number\" [(ngModel)]=\"model.value\"/></div></div><div *ngSwitchCase=\"Type.DECIMAL\"><input type=\"number\" [(ngModel)]=\"model.value\"/></div><div *ngSwitchCase=\"Type.STR\"><input class=\"option-value-str-input\" type=\"text\" [(ngModel)]=\"model.value\"/></div><div *ngSwitchCase=\"Type.TRANS_STR\"><trans-str [(translations)]=\"model.value\"></trans-str></div></div><div class=\"field two wide\"><label>Order</label><input class=\"option-order-input\" type=\"number\" placeholder=\"order\" [value]=\"model.order\" (change)=\"setOrder($event.target.value)\"/></div><sui-checkbox class=\"field three wide option-remove\" [ngModelOptions]=\"{standalone: true}\" [(ngModel)]=\"model.isMarkedAsRemoved\" [isDisabled]=\"!isCanBeRestored\">Remove</sui-checkbox></section>";

/***/ }),

/***/ 1091:
/***/ (function(module, exports) {

module.exports = ".fields.marked-as-removed {\n  opacity: 0.2; }\n\n.fields sui-checkbox {\n  display: flex !important;\n  align-self: center;\n  margin-top: 15px !important; }\n"

/***/ }),

/***/ 1092:
/***/ (function(module, exports, __webpack_require__) {

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
function asyncShowLoadingBar(target, propertyKey, descriptor) {
    let originalMethod = descriptor.value;
    descriptor.value = function (...args) {
        return __awaiter(this, void 0, void 0, function* () {
            this.loadingBarService.start();
            let result = yield originalMethod.apply(this, args);
            this.loadingBarService.complete();
            return result;
        });
    };
    return descriptor;
}
exports.asyncShowLoadingBar = asyncShowLoadingBar;


/***/ }),

/***/ 1093:
/***/ (function(module, exports, __webpack_require__) {

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
/** It will break without the semicolons. */
function asyncWithNotify(messages) {
    return (target, propertyKey, descriptor) => {
        let originalMethod = descriptor.value;
        descriptor.value = function (...args) {
            return __awaiter(this, void 0, void 0, function* () {
                let notifyService = this.notifyService;
                let result;
                try {
                    result = yield originalMethod.apply(this, args);
                    if (messages.onSuccessMsg !== undefined) {
                        notifyService.success(messages.onSuccessMsg);
                    }
                }
                catch (error) {
                    notifyService.error(messages.onErrorMsg, error);
                }
                return result;
            });
        };
        return descriptor;
    };
}
exports.asyncWithNotify = asyncWithNotify;


/***/ }),

/***/ 1094:
/***/ (function(module, exports) {

module.exports = "<!DOCTYPE html><ng2-slim-loading-bar [color]=\"&quot;#0ee8b9&quot;\" [height]=\"&quot;2px&quot;\"></ng2-slim-loading-bar><simple-notifications></simple-notifications><form class=\"ui form\" #clsForm=\"ngForm\"><h4 class=\"ui dividing header\">Attribute class</h4><section class=\"field four wide\" id=\"cls-code\"><label>Class code</label><input type=\"text\" name=\"code\" required placeholder=\"unique_class_code\" [(ngModel)]=\"model.code\"></section><section class=\"field four wide\" id=\"cls-type\"><label>Attribute class type</label><sui-select class=\"selection\" placeholder=\"Select a type\" [(ngModel)]=\"model.type\" [isDisabled]=\"model.isSaved\" [ngModelOptions]=\"{standalone: true}\" [optionFormatter]=\"selectTypeOptionFormatter\"><sui-select-option [value]=\"Type.INT\"></sui-select-option><sui-select-option [value]=\"Type.DECIMAL\"></sui-select-option><sui-select-option [value]=\"Type.TRANS_STR\"></sui-select-option><sui-select-option [value]=\"Type.STR\"></sui-select-option></sui-select></section><section class=\"field four wide\" id=\"cls-name\"><label>Name</label><trans-str [(translations)]=\"model.name\"></trans-str></section><section class=\"field four wide\" id=\"cls-product-type\"><label>Product type</label><sui-select class=\"selection\" placeholder=\"Select a type\" [(ngModel)]=\"model.productType\" [ngModelOptions]=\"{standalone: true}\" [optionFormatter]=\"selectProductTypeOptionFormatter\"><sui-select-option *ngFor=\"let productType of productTypeList\" [value]=\"productType\"></sui-select-option></sui-select></section><h4 class=\"ui dividing header\">Options</h4><section id=\"cls-options\"><div #options></div><button class=\"ui basic button\" id=\"add-option\" type=\"button\" (click)=\"addOption()\"><i class=\"add circle icon\"></i>Add an option</button></section><div class=\"ui divider\"></div><section id=\"cls-network-buttons\"><button class=\"ui positive button large right labeled icon\" id=\"cls-save-button\" type=\"submit\" (click)=\"save()\" *ngIf=\"model.isSaved\" [disabled]=\"!clsForm.form.valid\"><i class=\"save icon\"></i>Save</button><button class=\"ui positive button large right labeled icon\" id=\"cls-create-button\" type=\"submit\" (click)=\"create()\" *ngIf=\"!model.isSaved\" [disabled]=\"!clsForm.form.valid\"><i class=\"save icon\"></i>Create</button></section></form>";

/***/ }),

/***/ 1095:
/***/ (function(module, exports) {

module.exports = "#cls-name {\n  min-width: 450px; }\n\ninput.ng-touched.ng-invalid {\n  border-color: #e0b4b4 !important;\n  border-left: 4px solid #d65a5a !important;\n  background: #fff6f6 !important;\n  color: #9f3a38 !important; }\n  input.ng-touched.ng-invalid:hover {\n    border-color: #e0b4b4 !important;\n    border-left: 4px solid #d65a5a !important; }\n  input.ng-touched.ng-invalid:focus {\n    border-color: #e0b4b4 !important;\n    border-left: 4px solid #d65a5a !important; }\n\ninput.ng-untouched.ng-invalid {\n  border-left: 4px solid #d65a5a !important; }\n  input.ng-untouched.ng-invalid:hover {\n    border-left: 4px solid #d65a5a !important; }\n  input.ng-untouched.ng-invalid:focus {\n    border-left: 4px solid #d65a5a !important; }\n\n*:focus {\n  outline: none; }\n\n.field input:hover {\n  border-color: rgba(34, 36, 38, 0.35) !important; }\n\n.field input:focus {\n  border-color: #85B7D9 !important; }\n\n.shuup-toolbar form .btn-toolbar .btn-group .btn.btn-success {\n  display: none; }\n\n.shuup-toolbar form .btn-toolbar .btn-group .dropdown-toggle.btn-success {\n  display: none; }\n\n.content-block {\n  width: auto;\n  margin-right: 15px !important;\n  margin-left: 28px; }\n"

/***/ }),

/***/ 1096:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
let IterateEnumPipe = class IterateEnumPipe {
    transform(enumObj, args) {
        let enumForIteration = [];
        let enumIndexes = Object.keys(enumObj).filter(Number);
        for (let enumIndex of enumIndexes) {
            enumForIteration.push({ value: enumIndex, name: enumObj[enumIndex] });
        }
        return enumForIteration;
    }
};
IterateEnumPipe = __decorate([
    core_1.Pipe({ name: 'iterEnum' })
], IterateEnumPipe);
exports.IterateEnumPipe = IterateEnumPipe;


/***/ }),

/***/ 129:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var Type;
(function (Type) {
    Type[Type["INT"] = 1] = "INT";
    Type[Type["DECIMAL"] = 3] = "DECIMAL";
    Type[Type["TRANS_STR"] = 20] = "TRANS_STR";
    Type[Type["STR"] = 21] = "STR";
})(Type = exports.Type || (exports.Type = {}));


/***/ }),

/***/ 208:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const cls_json_service_1 = __webpack_require__(451);
const csrf_service_1 = __webpack_require__(210);
const http_1 = __webpack_require__(72);
let ClsNetworkService = class ClsNetworkService {
    constructor(jsonSerializer, csrfService, http) {
        this.jsonSerializer = jsonSerializer;
        this.csrfService = csrfService;
        this.http = http;
    }
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let clsJson = yield this.http.get(`/api/attrim/classes/${pk}/`)
                .first()
                .toPromise();
            let cls = yield this.jsonSerializer.deserialize(clsJson);
            return cls;
        });
    }
    save(cls) {
        return __awaiter(this, void 0, void 0, function* () {
            let clsJson = this.jsonSerializer.serialize(cls);
            let clsSavedJson = yield this.http.patch(`/api/attrim/classes/${cls.pk}/`, clsJson, this.csrfService.getHttpOptions())
                .first()
                .toPromise();
            let clsSaved = yield this.jsonSerializer.deserialize(clsSavedJson);
            return clsSaved;
        });
    }
    create(cls) {
        return __awaiter(this, void 0, void 0, function* () {
            let clsJson = this.jsonSerializer.serialize(cls);
            let clsJsonCreated = yield this.http.post(`/api/attrim/classes/`, clsJson, this.csrfService.getHttpOptions())
                .first()
                .toPromise();
            let clsCreated = yield this.jsonSerializer.deserialize(clsJsonCreated);
            return clsCreated;
        });
    }
};
ClsNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [cls_json_service_1.ClsJsonSerializerService,
        csrf_service_1.CsrfService,
        http_1.HttpClient])
], ClsNetworkService);
exports.ClsNetworkService = ClsNetworkService;


/***/ }),

/***/ 209:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const product_type_json_service_1 = __webpack_require__(453);
const http_1 = __webpack_require__(72);
let ProductTypeNetworkService = class ProductTypeNetworkService {
    constructor(http, jsonSerializer) {
        this.http = http;
        this.jsonSerializer = jsonSerializer;
    }
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let productTypeJson = yield this.http
                .get(`/api/attrim/product-types/${pk}/`)
                .first()
                .toPromise();
            return this.jsonSerializer.deserialize(productTypeJson);
        });
    }
    getAll() {
        return __awaiter(this, void 0, void 0, function* () {
            let typeJsonArray = yield this.http
                .get('/api/attrim/product-types/')
                .first()
                .toPromise();
            return this.jsonSerializer.deserializeArray(typeJsonArray);
        });
    }
};
ProductTypeNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.HttpClient,
        product_type_json_service_1.ProductTypeJsonSerializerService])
], ProductTypeNetworkService);
exports.ProductTypeNetworkService = ProductTypeNetworkService;


/***/ }),

/***/ 210:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
const cookie_service_1 = __webpack_require__(454);
const http_1 = __webpack_require__(72);
let CsrfService = class CsrfService {
    constructor(cookieService) {
        this.cookieService = cookieService;
    }
    getHttpOptions() {
        let headers = new http_1.HttpHeaders({
            'Content-Type': 'application/json',
            'X-CSRFToken': this.cookieService.getByName('csrftoken'),
        });
        let options = { headers: headers };
        return options;
    }
};
CsrfService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [cookie_service_1.CookieService])
], CsrfService);
exports.CsrfService = CsrfService;


/***/ }),

/***/ 446:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const type_enum_decorator_1 = __webpack_require__(447);
const type_enum_1 = __webpack_require__(129);
const core_2 = __webpack_require__(1);
const option_model_1 = __webpack_require__(448);
const option_service_1 = __webpack_require__(449);
const core_3 = __webpack_require__(1);
let OptionFormComponent = class OptionFormComponent {
    constructor(networkService, changeDetector) {
        this.networkService = networkService;
        this.changeDetector = changeDetector;
        this.isCanBeRestored = true;
    }
    initForm(args) {
        return __awaiter(this, void 0, void 0, function* () {
            this.initChildComponents();
            let option;
            if (args.optionPk !== undefined) {
                option = yield this.networkService.get(args.optionPk);
            }
            else {
                option = new option_model_1.Option({ type: args.type, clsPk: args.clsPk });
            }
            this.model = option;
            this.updateNgSwitch();
        });
    }
    setOrder(valueRaw) {
        this.model.order = Number(valueRaw);
    }
    save() {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.model.isMarkedAsRemoved) {
                yield this.networkService.delete(this.model);
                this.isCanBeRestored = false;
            }
            else if (this.model.isSaved) {
                let optionSaved = yield this.networkService.save(this.model);
                this.model = optionSaved;
            }
            else {
                let optionCreated = yield this.networkService.create(this.model);
                this.model = optionCreated;
            }
        });
    }
    /**
     * For TRANS_STR init, also required if it's an edit form and the edited Option
     * has a TRANS_STR type. Otherwise the ngModel binding won't work.
     */
    initChildComponents() {
        this.model = new option_model_1.Option({ type: type_enum_1.Type.TRANS_STR });
        this.changeDetector.detectChanges();
    }
    updateNgSwitch() {
        this.changeDetector.detectChanges();
    }
};
OptionFormComponent = __decorate([
    core_1.Component({
        selector: 'option-form',
        template: __webpack_require__(1090),
        styles: [__webpack_require__(1091)],
        // the encapsulation is screwed up for dynamic components in 4.0.3
        encapsulation: core_3.ViewEncapsulation.None,
    }),
    type_enum_decorator_1.TypeEnumDecorator,
    __metadata("design:paramtypes", [option_service_1.OptionNetworkService,
        core_2.ChangeDetectorRef])
], OptionFormComponent);
exports.OptionFormComponent = OptionFormComponent;


/***/ }),

/***/ 447:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
const type_enum_1 = __webpack_require__(129);
/**
 * Allows to use the `Type` enum directly in templates.
 */
function TypeEnumDecorator(constructor) {
    constructor.prototype.Type = type_enum_1.Type;
}
exports.TypeEnumDecorator = TypeEnumDecorator;


/***/ }),

/***/ 448:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
const type_enum_1 = __webpack_require__(129);
class Option {
    constructor(args) {
        this.pk = null;
        this.clsPk = null;
        this.order = null;
        /**
         * Must have a default object `{}`, otherwise it'll screw up
         * the sharing of the `value` between OptionComponent and its child
         * TransStrComponent.
         */
        this.value = {};
        this.isMarkedAsRemoved = false;
        this.isSaved = false;
        this.pk = args.pk ? args.pk : this.pk;
        this.clsPk = args.clsPk ? args.clsPk : this.clsPk;
        this.type = args.type;
        this.order = args.order ? args.order : this.order;
        this.value = args.value ? args.value : this.getDefaultValue(this.type);
        if (args.isMarkedAsRemoved) {
            this.isMarkedAsRemoved = args.isMarkedAsRemoved;
        }
        this.isSaved = args.isSaved ? args.isSaved : this.isSaved;
    }
    getDefaultValue(type) {
        let value;
        switch (type) {
            case type_enum_1.Type.INT:
                value = 0;
                break;
            case type_enum_1.Type.DECIMAL:
                value = 0.0;
                break;
            case type_enum_1.Type.TRANS_STR:
                // Must have a default object `{}`, otherwise it'll screw up
                // the sharing of the `value` between OptionComponent and its child
                // TransStrComponent.
                value = {};
                break;
            case type_enum_1.Type.STR:
                value = '';
                break;
            default:
                throw Error('wrong type');
        }
        return value;
    }
}
exports.Option = Option;


/***/ }),

/***/ 449:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const option_json_service_1 = __webpack_require__(450);
const csrf_service_1 = __webpack_require__(210);
const http_1 = __webpack_require__(72);
let OptionNetworkService = class OptionNetworkService {
    constructor(jsonSerializer, csrfService, http) {
        this.jsonSerializer = jsonSerializer;
        this.csrfService = csrfService;
        this.http = http;
    }
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionJson = yield this.http.get(`/api/attrim/options/${pk}/`)
                .first()
                .toPromise();
            let option = yield this.jsonSerializer.deserialize(optionJson);
            return option;
        });
    }
    save(option) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionJson = this.jsonSerializer.serialize(option);
            let optionSavedJson = yield this.http.patch(`/api/attrim/options/${option.pk}/`, optionJson, this.csrfService.getHttpOptions())
                .first()
                .toPromise();
            let optionSaved = yield this.jsonSerializer.deserialize(optionSavedJson);
            return optionSaved;
        });
    }
    create(option) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionJson = this.jsonSerializer.serialize(option);
            let optionCreatedJson = yield this.http.post(`/api/attrim/options/`, optionJson, this.csrfService.getHttpOptions())
                .first()
                .toPromise();
            let optionCreated = yield this.jsonSerializer.deserialize(optionCreatedJson);
            return optionCreated;
        });
    }
    delete(option) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.http.delete(`/api/attrim/options/${option.pk}/`, this.csrfService.getHttpOptions())
                .first()
                .toPromise();
        });
    }
};
OptionNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [option_json_service_1.OptionJsonSerializerService,
        csrf_service_1.CsrfService,
        http_1.HttpClient])
], OptionNetworkService);
exports.OptionNetworkService = OptionNetworkService;


/***/ }),

/***/ 450:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const option_model_1 = __webpack_require__(448);
const cls_service_1 = __webpack_require__(208);
let OptionJsonSerializerService = class OptionJsonSerializerService {
    constructor(clsService) {
        this.clsService = clsService;
    }
    serialize(option) {
        if (option.clsPk === null) {
            throw TypeError('Option to serialize must have a class assigned.');
        }
        let optionJson = {
            pk: option.pk,
            cls: option.clsPk,
            value: option.value,
            order: option.order,
        };
        return optionJson;
    }
    deserialize(optionJson) {
        return __awaiter(this, void 0, void 0, function* () {
            let option = new option_model_1.Option({
                pk: optionJson.pk,
                clsPk: optionJson.cls,
                type: (yield this.clsService.get(optionJson.cls)).type,
                value: optionJson.value,
                order: optionJson.order,
                isSaved: true,
            });
            return option;
        });
    }
};
OptionJsonSerializerService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [cls_service_1.ClsNetworkService])
], OptionJsonSerializerService);
exports.OptionJsonSerializerService = OptionJsonSerializerService;


/***/ }),

/***/ 451:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const core_1 = __webpack_require__(1);
const cls_model_1 = __webpack_require__(452);
const product_type_service_1 = __webpack_require__(209);
let ClsJsonSerializerService = class ClsJsonSerializerService {
    constructor(productTypeService) {
        this.productTypeService = productTypeService;
    }
    serialize(cls) {
        let clsJson = {
            pk: cls.pk,
            code: cls.code,
            type: cls.type,
            name: cls.name,
            product_type: cls.productType.pk,
        };
        return clsJson;
    }
    deserialize(clsJson) {
        return __awaiter(this, void 0, void 0, function* () {
            let cls = new cls_model_1.Cls({
                pk: clsJson.pk,
                code: clsJson.code,
                type: clsJson.type,
                name: clsJson.name,
                productType: yield this.deserializeProductType(clsJson),
                optionsPk: clsJson.options,
                isSaved: true,
            });
            return cls;
        });
    }
    deserializeProductType(clsJson) {
        return __awaiter(this, void 0, void 0, function* () {
            let productTypePk = clsJson.product_type;
            return yield this.productTypeService.get(productTypePk);
        });
    }
};
ClsJsonSerializerService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [product_type_service_1.ProductTypeNetworkService])
], ClsJsonSerializerService);
exports.ClsJsonSerializerService = ClsJsonSerializerService;


/***/ }),

/***/ 452:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
class Cls {
    constructor(args) {
        this.pk = null;
        this.name = {};
        this.optionsPk = [];
        this.isSaved = false;
        this.pk = args.pk ? args.pk : this.pk;
        this.code = args.code;
        this.type = args.type;
        this.name = args.name ? args.name : this.name;
        this.productType = args.productType;
        this.optionsPk = args.optionsPk ? args.optionsPk : this.optionsPk;
        this.isSaved = args.isSaved ? args.isSaved : this.isSaved;
    }
}
exports.Cls = Cls;


/***/ }),

/***/ 453:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
let ProductTypeJsonSerializerService = class ProductTypeJsonSerializerService {
    deserialize(productTypeJson) {
        let productType = {
            pk: productTypeJson.id,
            name: productTypeJson.translations[window.DJANGO.defaultLang]['name'],
        };
        return productType;
    }
    deserializeArray(productTypeArrayJson) {
        let productTypeArray = [];
        for (let productTypeJson of productTypeArrayJson) {
            let productType = {
                pk: productTypeJson.id,
                name: productTypeJson.translations[window.DJANGO.defaultLang]['name'],
            };
            productTypeArray.push(productType);
        }
        return productTypeArray;
    }
};
ProductTypeJsonSerializerService = __decorate([
    core_1.Injectable()
], ProductTypeJsonSerializerService);
exports.ProductTypeJsonSerializerService = ProductTypeJsonSerializerService;


/***/ }),

/***/ 454:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
let CookieService = class CookieService {
    getByName(name) {
        let nameNeedle = `${name}=`;
        let cookies = document.cookie.split(';');
        for (let cookieStrRaw of cookies) {
            let cookieStr = cookieStrRaw.trim();
            let isCookieNameFound = cookieStr.search(nameNeedle) === 0;
            if (isCookieNameFound) {
                let cookieValueIndexStart = nameNeedle.length;
                let cookieValueIndexEnd = cookieStr.length;
                let cookieValue = cookieStr.substring(cookieValueIndexStart, cookieValueIndexEnd);
                return cookieValue;
            }
        }
        return null;
    }
};
CookieService = __decorate([
    core_1.Injectable()
], CookieService);
exports.CookieService = CookieService;


/***/ }),

/***/ 455:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(1);
const angular2_notifications_1 = __webpack_require__(123);
let NotifyService = class NotifyService {
    constructor(service) {
        this.service = service;
        this.config = {
            timeOut: 5000,
            showProgressBar: true,
            pauseOnHover: true,
            clickToClose: true,
        };
    }
    error(title, content = '') {
        this.service.error(title, content, this.config);
    }
    success(title, content = '') {
        this.service.success(title, content, this.config);
    }
};
NotifyService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [angular2_notifications_1.NotificationsService])
], NotifyService);
exports.NotifyService = NotifyService;


/***/ })

},[1083]);