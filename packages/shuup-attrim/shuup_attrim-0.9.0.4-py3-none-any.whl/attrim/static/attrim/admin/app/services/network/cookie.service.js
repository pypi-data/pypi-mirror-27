"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
let CookieService = class CookieService {
    getByName(name) {
        let nameNeedle = `${name}=`;
        let cookies = document.cookie.split(';');
        for (let cookieStrRaw of cookies) {
            let cookieStr = cookieStrRaw.trim();
            let isCookieNameFound = cookieStr.search(nameNeedle) === 0;
            if (isCookieNameFound) {
                let cookieValueIndexStart = nameNeedle.length;
                let cookieValueIndexEnd = cookieStr.length;
                let cookieValue = cookieStr.substring(cookieValueIndexStart, cookieValueIndexEnd);
                return cookieValue;
            }
        }
        return null;
    }
};
CookieService = __decorate([
    core_1.Injectable()
], CookieService);
exports.CookieService = CookieService;
//# sourceMappingURL=cookie.service.js.map