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
const core_1 = require("@angular/core");
const type_enum_1 = require("app/type.enum");
const option_form_comp_1 = require("app/cls-form/fields/option-form.comp");
const core_2 = require("@angular/core");
const core_3 = require("@angular/core");
const core_4 = require("@angular/core");
const type_enum_decorator_1 = require("app/decorators/type.enum.decorator");
const core_5 = require("@angular/core");
const cls_model_1 = require("app/models/cls.model");
const cls_service_1 = require("app/services/network/cls.service");
const product_type_service_1 = require("app/services/network/product-type.service");
const notify_service_1 = require("app/services/notify.service");
const ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
const async_show_loading_bar_decorator_1 = require("app/decorators/async-show-loading-bar.decorator");
const async_notify_on_decorator_1 = require("app/decorators/async-notify-on.decorator");
// TODO refactor?
let ClsFormComponent = class ClsFormComponent {
    // noinspection JSUnusedLocalSymbols
    constructor(networkService, productTypeService, notifyService, loadingBarService, componentFactoryResolver) {
        this.networkService = networkService;
        this.productTypeService = productTypeService;
        this.notifyService = notifyService;
        this.loadingBarService = loadingBarService;
        this.componentFactoryResolver = componentFactoryResolver;
        this.optionRefSet = new Set();
    }
    ngOnInit() {
        let clsStubForRender = new cls_model_1.Cls({
            code: '',
            type: type_enum_1.Type.INT,
            productType: { name: '', pk: 0 },
        });
        this.model = clsStubForRender;
        // noinspection JSIgnoredPromiseFromCall
        this.initForm();
    }
    setType(typeValueRaw) {
        let typeNew = Number(typeValueRaw);
        this.model.type = typeNew;
    }
    setProductType(productTypePkRaw) {
        let pkSelected = Number(productTypePkRaw);
        this.model.productType = this.productTypeList
            .find(productType => productType.pk === pkSelected);
    }
    addOption(args) {
        let ref = this.createOptionComponent();
        if (args) {
            // noinspection JSIgnoredPromiseFromCall
            ref.instance.initForm(args);
        }
        else {
            // noinspection JSIgnoredPromiseFromCall
            ref.instance.initForm({ type: this.model.type, clsPk: this.model.pk });
        }
        this.optionRefSet.add(ref);
    }
    save() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsSaved = yield this.saveCls();
            yield this.saveOptions(clsSaved.pk);
        });
    }
    create() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsCreated = yield this.networkService.create(this.model);
            yield this.saveOptions(clsCreated.pk);
            location.assign(`/sa/attrim/${clsCreated.pk}/`);
        });
    }
    saveCls() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsSaved = yield this.networkService.save(this.model);
            this.model = clsSaved;
            return clsSaved;
        });
    }
    saveOptions(clsPk) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionSavePromises = [];
            for (let optionRef of this.optionRefSet) {
                optionRef.instance.model.clsPk = clsPk;
                let savePromise = optionRef.instance.save();
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
            // TODO use an async pipe with productTypeService.getAll() and remove clsStubForRender
            this.productTypeList = yield this.productTypeService.getAll();
        });
    }
    loadFormDataFromServer() {
        return __awaiter(this, void 0, void 0, function* () {
            let clsPkToEdit = window.DJANGO.clsPrimaryKey;
            let clsToEdit = yield this.networkService.get(clsPkToEdit);
            this.model = clsToEdit;
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
};
__decorate([
    core_4.ViewChild('options', { read: core_3.ViewContainerRef }),
    __metadata("design:type", core_3.ViewContainerRef
    // noinspection JSUnusedLocalSymbols
    )
], ClsFormComponent.prototype, "optionsContainerRef", void 0);
__decorate([
    async_show_loading_bar_decorator_1.asyncShowLoadingBar,
    async_notify_on_decorator_1.asyncNotifyOn({ success: 'The saving complete', error: 'The saving failed' }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ClsFormComponent.prototype, "save", null);
__decorate([
    async_show_loading_bar_decorator_1.asyncShowLoadingBar,
    async_notify_on_decorator_1.asyncNotifyOn({ error: 'Creation failed' }),
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
    async_notify_on_decorator_1.asyncNotifyOn({ error: 'Network error during product types retrieving' }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ClsFormComponent.prototype, "initProductTypeList", null);
ClsFormComponent = __decorate([
    core_1.Component({
        selector: 'cls-form',
        moduleId: module.id,
        templateUrl: 'cls-form.comp.html',
        styleUrls: ['cls-form.comp.css'],
        encapsulation: core_5.ViewEncapsulation.None,
    }),
    type_enum_decorator_1.TypeEnumDecorator,
    __metadata("design:paramtypes", [cls_service_1.ClsNetworkService,
        product_type_service_1.ProductTypeNetworkService,
        notify_service_1.NotifyService,
        ng2_slim_loading_bar_1.SlimLoadingBarService,
        core_2.ComponentFactoryResolver])
], ClsFormComponent);
exports.ClsFormComponent = ClsFormComponent;
//# sourceMappingURL=cls-form.comp.js.map