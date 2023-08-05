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
const cls_model_1 = require("app/models/cls.model");
const product_type_service_1 = require("app/services/network/product-type.service");
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
//# sourceMappingURL=cls-json.service.js.map