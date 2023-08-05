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
const option_model_1 = require("app/models/option.model");
const cls_service_1 = require("app/services/network/cls.service");
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
//# sourceMappingURL=option-json.service.js.map