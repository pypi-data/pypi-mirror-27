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
const core_1 = require("@angular/core");
const core_2 = require("@angular/core");
const core_3 = require("@angular/core");
const core_4 = require("@angular/core");
const core_5 = require("@angular/core");
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
        moduleId: module.id,
        templateUrl: 'trans-str.comp.html',
        styleUrls: ['trans-str.comp.css'],
        // the encapsulation is screwed up for dynamic components in 4.0.3
        encapsulation: core_5.ViewEncapsulation.None,
    })
], TransStrComponent);
exports.TransStrComponent = TransStrComponent;
//# sourceMappingURL=trans-str.comp.js.map