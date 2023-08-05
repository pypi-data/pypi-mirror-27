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
const type_enum_decorator_1 = require("app/decorators/type.enum.decorator");
const type_enum_1 = require("app/type.enum");
const core_2 = require("@angular/core");
const option_model_1 = require("app/models/option.model");
const option_service_1 = require("app/services/network/option.service");
const core_3 = require("@angular/core");
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
     * has TRANS_STR type. Otherwise the ngModel binding won't work.
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
        moduleId: module.id,
        templateUrl: 'option-form.comp.html',
        styleUrls: ['option-form.comp.css'],
        // the encapsulation is screwed up for dynamic components in 4.0.3
        encapsulation: core_3.ViewEncapsulation.None,
    }),
    type_enum_decorator_1.TypeEnumDecorator,
    __metadata("design:paramtypes", [option_service_1.OptionNetworkService,
        core_2.ChangeDetectorRef])
], OptionFormComponent);
exports.OptionFormComponent = OptionFormComponent;
//# sourceMappingURL=option-form.comp.js.map