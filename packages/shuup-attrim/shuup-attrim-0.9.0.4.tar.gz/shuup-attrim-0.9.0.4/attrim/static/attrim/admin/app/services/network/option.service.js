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
const option_json_service_1 = require("app/services/network/serializers/option-json.service");
const http_1 = require("@angular/http");
const csrf_service_1 = require("app/services/network/csrf.service");
let OptionNetworkService = class OptionNetworkService {
    constructor(jsonSerializer, csrfService, http) {
        this.jsonSerializer = jsonSerializer;
        this.csrfService = csrfService;
        this.http = http;
    }
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let response = yield this.http.get(`/api/attrim/options/${pk}/`)
                .first()
                .toPromise();
            let optionJson = response.json();
            let option = yield this.jsonSerializer.deserialize(optionJson);
            return option;
        });
    }
    save(option) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionJson = this.jsonSerializer.serialize(option);
            let response = yield this.http.patch(`/api/attrim/options/${option.pk}/`, optionJson, this.csrfService.getRequestOptions())
                .first()
                .toPromise();
            let optionSavedJson = response.json();
            let optionSaved = yield this.jsonSerializer.deserialize(optionSavedJson);
            return optionSaved;
        });
    }
    create(option) {
        return __awaiter(this, void 0, void 0, function* () {
            let optionJson = this.jsonSerializer.serialize(option);
            let response = yield this.http.post(`/api/attrim/options/`, optionJson, this.csrfService.getRequestOptions())
                .first()
                .toPromise();
            let optionCreatedJson = response.json();
            let optionCreated = yield this.jsonSerializer.deserialize(optionCreatedJson);
            return optionCreated;
        });
    }
    delete(option) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.http.delete(`/api/attrim/options/${option.pk}/`, this.csrfService.getRequestOptions())
                .first()
                .toPromise();
        });
    }
};
OptionNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [option_json_service_1.OptionJsonSerializerService,
        csrf_service_1.CsrfService,
        http_1.Http])
], OptionNetworkService);
exports.OptionNetworkService = OptionNetworkService;
//# sourceMappingURL=option.service.js.map