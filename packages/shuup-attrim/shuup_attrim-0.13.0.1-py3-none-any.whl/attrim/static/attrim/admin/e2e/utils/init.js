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
const protractor_1 = require("protractor");
const navigation_1 = require("./navigation");
function init() {
    return __awaiter(this, void 0, void 0, function* () {
        yield navigation_1.login();
        // otherwise shuup may switch to a mobile makeup and protractor testing will
        // become even more nasty
        yield protractor_1.browser.driver.manage().window().setSize(1900, 1000);
    });
}
exports.init = init;
//# sourceMappingURL=init.js.map