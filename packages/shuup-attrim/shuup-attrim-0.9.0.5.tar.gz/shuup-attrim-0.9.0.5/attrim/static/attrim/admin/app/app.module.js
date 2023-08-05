"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
const platform_browser_1 = require("@angular/platform-browser");
const app_comp_1 = require("app/app.comp");
const trans_str_comp_1 = require("app/cls-form/fields/trans-str.comp");
const forms_1 = require("@angular/forms");
const ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
const cls_form_comp_1 = require("app/cls-form/cls-form.comp");
const option_form_comp_1 = require("app/cls-form/fields/option-form.comp");
const iter_enum_pipe_1 = require("app/iter-enum.pipe");
const cls_service_1 = require("app/services/network/cls.service");
const cls_json_service_1 = require("app/services/network/serializers/cls-json.service");
const angular2_notifications_1 = require("angular2-notifications");
const notify_service_1 = require("app/services/notify.service");
const product_type_service_1 = require("app/services/network/product-type.service");
const option_json_service_1 = require("app/services/network/serializers/option-json.service");
const option_service_1 = require("app/services/network/option.service");
const http_1 = require("@angular/http");
const http_2 = require("@angular/http");
const product_type_json_service_1 = require("app/services/network/serializers/product-type-json.service");
const cookie_service_1 = require("app/services/network/cookie.service");
const csrf_service_1 = require("app/services/network/csrf.service");
const animations_1 = require("@angular/platform-browser/animations");
const angular2_notifications_2 = require("angular2-notifications");
const angular2_semantic_ui_1 = require("angular2-semantic-ui");
let AppModule = class AppModule {
};
AppModule = __decorate([
    core_1.NgModule({
        imports: [
            platform_browser_1.BrowserModule, forms_1.FormsModule, http_1.HttpModule, http_2.JsonpModule, animations_1.BrowserAnimationsModule,
            ng2_slim_loading_bar_1.SlimLoadingBarModule.forRoot(), angular2_notifications_2.SimpleNotificationsModule.forRoot(),
            angular2_semantic_ui_1.L_SEMANTIC_UI_MODULE,
        ],
        declarations: [
            app_comp_1.AppComponent, cls_form_comp_1.ClsFormComponent, option_form_comp_1.OptionFormComponent, trans_str_comp_1.TransStrComponent,
            iter_enum_pipe_1.IterateEnumPipe,
        ],
        entryComponents: [option_form_comp_1.OptionFormComponent],
        exports: [iter_enum_pipe_1.IterateEnumPipe],
        providers: [
            cls_service_1.ClsNetworkService, cls_json_service_1.ClsJsonSerializerService,
            product_type_service_1.ProductTypeNetworkService, notify_service_1.NotifyService, angular2_notifications_1.NotificationsService,
            option_json_service_1.OptionJsonSerializerService, option_service_1.OptionNetworkService,
            product_type_json_service_1.ProductTypeJsonSerializerService, cookie_service_1.CookieService, csrf_service_1.CsrfService,
        ],
        bootstrap: [app_comp_1.AppComponent],
    })
], AppModule);
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map