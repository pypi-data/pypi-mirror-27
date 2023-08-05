"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
function asyncNotifyOn(messages) {
    return (target, propertyKey, descriptor) => {
        let originalMethod = descriptor.value;
        descriptor.value = function (...args) {
            return __awaiter(this, void 0, void 0, function* () {
                let result;
                try {
                    result = yield originalMethod.apply(this, args);
                    if (messages.success !== null) {
                        this.notifyService.success(messages.success);
                    }
                }
                catch (error) {
                    this.notifyService.error(messages.error, error);
                }
                return result;
            });
        };
        return descriptor;
    };
}
exports.asyncNotifyOn = asyncNotifyOn;
//# sourceMappingURL=notify.serivce.js.map