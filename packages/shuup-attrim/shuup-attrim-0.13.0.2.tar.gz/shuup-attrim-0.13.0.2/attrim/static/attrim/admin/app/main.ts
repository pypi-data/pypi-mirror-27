import 'rxjs/Rx'
import 'reflect-metadata'
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic'

import {AppModule} from 'app/app.module'


//noinspection JSIgnoredPromiseFromCall
platformBrowserDynamic().bootstrapModule(AppModule)
