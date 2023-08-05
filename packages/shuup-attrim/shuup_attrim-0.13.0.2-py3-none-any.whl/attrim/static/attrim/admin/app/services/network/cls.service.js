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
const cls_json_service_1 = require("app/services/network/serializers/cls-json.service");
const http_1 = require("@angular/http");
const csrf_service_1 = require("app/services/network/csrf.service");
let ClsNetworkService = class ClsNetworkService {
    constructor(jsonSerializer, csrfService, http) {
        this.jsonSerializer = jsonSerializer;
        this.csrfService = csrfService;
        this.http = http;
    }
    get(pk) {
        return __awaiter(this, void 0, void 0, function* () {
            let response = yield this.http.get(`/api/attrim/classes/${pk}/`)
                .first()
                .toPromise();
            let clsJson = response.json();
            let cls = yield this.jsonSerializer.deserialize(clsJson);
            return cls;
        });
    }
    save(cls) {
        return __awaiter(this, void 0, void 0, function* () {
            let clsJson = this.jsonSerializer.serialize(cls);
            let response = yield this.http.patch(`/api/attrim/classes/${cls.pk}/`, clsJson, this.csrfService.getRequestOptions())
                .first()
                .toPromise();
            let clsSavedJson = response.json();
            let clsSaved = yield this.jsonSerializer.deserialize(clsSavedJson);
            return clsSaved;
        });
    }
    create(cls) {
        return __awaiter(this, void 0, void 0, function* () {
            let clsJson = this.jsonSerializer.serialize(cls);
            let response = yield this.http.post(`/api/attrim/classes/`, clsJson, this.csrfService.getRequestOptions())
                .first()
                .toPromise();
            let clsJsonCreated = response.json();
            let clsCreated = yield this.jsonSerializer.deserialize(clsJsonCreated);
            return clsCreated;
        });
    }
};
ClsNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [cls_json_service_1.ClsJsonSerializerService,
        csrf_service_1.CsrfService,
        http_1.Http])
], ClsNetworkService);
exports.ClsNetworkService = ClsNetworkService;
//# sourceMappingURL=cls.service.js.map