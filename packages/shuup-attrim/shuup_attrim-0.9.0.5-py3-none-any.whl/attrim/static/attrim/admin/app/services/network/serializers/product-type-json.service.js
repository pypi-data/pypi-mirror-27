"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
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
//# sourceMappingURL=product-type-json.service.js.map