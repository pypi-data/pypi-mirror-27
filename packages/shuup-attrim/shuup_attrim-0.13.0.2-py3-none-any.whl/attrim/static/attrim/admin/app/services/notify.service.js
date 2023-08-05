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
const angular2_notifications_1 = require("angular2-notifications");
let NotifyService = class NotifyService {
    constructor(service) {
        this.config = {
            timeOut: 5000,
            showProgressBar: true,
            pauseOnHover: true,
            clickToClose: true,
        };
        this.service = service;
    }
    error(title, content = '') {
        this.service.error(title, content, this.config);
    }
    success(title, content = '') {
        this.service.success(title, content, this.config);
    }
};
NotifyService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [angular2_notifications_1.NotificationsService])
], NotifyService);
exports.NotifyService = NotifyService;
//# sourceMappingURL=notify.service.js.map