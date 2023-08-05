import {NgModule}      from '@angular/core'
import {BrowserModule} from '@angular/platform-browser'
import {AppComponent}  from 'app/app.comp'
import {TransStrComponent} from 'app/cls-form/fields/trans-str.comp'
import {FormsModule} from '@angular/forms'
import {SlimLoadingBarModule} from 'ng2-slim-loading-bar'
import {ClsFormComponent} from 'app/cls-form/cls-form.comp'
import {OptionFormComponent} from 'app/cls-form/fields/option-form.comp'
import {IterateEnumPipe} from 'app/iter-enum.pipe'
import {ClsNetworkService} from 'app/services/network/cls.service'
import {ClsJsonSerializerService} from 'app/services/network/serializers/cls-json.service'
import {NotificationsService} from 'angular2-notifications'
import {NotifyService} from 'app/services/notify.service'
import {ProductTypeNetworkService} from 'app/services/network/product-type.service'
import {OptionJsonSerializerService} from 'app/services/network/serializers/option-json.service'
import {OptionNetworkService} from 'app/services/network/option.service'
import {HttpModule} from '@angular/http'
import {JsonpModule} from '@angular/http'
import {ProductTypeJsonSerializerService} from 'app/services/network/serializers/product-type-json.service'
import {CookieService} from 'app/services/network/cookie.service'
import {CsrfService} from 'app/services/network/csrf.service'
import {BrowserAnimationsModule} from '@angular/platform-browser/animations'
import {SimpleNotificationsModule} from 'angular2-notifications'
import {L_SEMANTIC_UI_MODULE} from 'angular2-semantic-ui'


@NgModule({
    imports: [
        BrowserModule, FormsModule, HttpModule, JsonpModule, BrowserAnimationsModule,
        SlimLoadingBarModule.forRoot(), SimpleNotificationsModule.forRoot(),
        L_SEMANTIC_UI_MODULE,
    ],
    declarations: [
        AppComponent, ClsFormComponent, OptionFormComponent, TransStrComponent,
        IterateEnumPipe,
    ],
    entryComponents: [OptionFormComponent],
    exports: [IterateEnumPipe],
    providers: [
        ClsNetworkService, ClsJsonSerializerService,
        ProductTypeNetworkService, NotifyService, NotificationsService,
        OptionJsonSerializerService, OptionNetworkService,
        ProductTypeJsonSerializerService, CookieService, CsrfService,
    ],
    bootstrap: [AppComponent],
})
export class AppModule { }
