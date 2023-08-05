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
const http_1 = require("@angular/http");
const cookie_service_1 = require("app/services/network/cookie.service");
const http_2 = require("@angular/http");
let CsrfService = class CsrfService {
    constructor(cookieService) {
        this.cookieService = cookieService;
    }
    getRequestOptions() {
        let headers = new http_2.Headers({
            'Content-Type': 'application/json',
            'X-CSRFToken': this.cookieService.getByName('csrftoken'),
        });
        return new http_1.RequestOptions({ headers: headers });
    }
};
CsrfService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [cookie_service_1.CookieService])
], CsrfService);
exports.CsrfService = CsrfService;
//# sourceMappingURL=csrf.service.js.map