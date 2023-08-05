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
const http_1 = require("@angular/http");
const product_type_json_service_1 = require("app/services/network/serializers/product-type-json.service");
let ProductTypeNetworkService = class ProductTypeNetworkService {
    constructor(http, jsonSerializer) {
        this.http = http;
        this.jsonSerializer = jsonSerializer;
    }
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let response = yield this.http.request(`/api/shuup/product_type/${pk}/`)
                .first()
                .toPromise();
            let productTypeJson = response.json();
            return this.jsonSerializer.deserialize(productTypeJson);
        });
    }
    getAll() {
        return __awaiter(this, void 0, void 0, function* () {
            let response = yield this.http.request('/api/shuup/product_type/')
                .first()
                .toPromise();
            let productTypeArrayJson = response.json();
            return this.jsonSerializer.deserializeArray(productTypeArrayJson);
        });
    }
};
ProductTypeNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Http,
        product_type_json_service_1.ProductTypeJsonSerializerService])
], ProductTypeNetworkService);
exports.ProductTypeNetworkService = ProductTypeNetworkService;
//# sourceMappingURL=product-type.service.js.map