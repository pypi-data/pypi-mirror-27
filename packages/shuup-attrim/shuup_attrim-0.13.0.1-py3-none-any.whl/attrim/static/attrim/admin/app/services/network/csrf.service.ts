import {Injectable} from '@angular/core'
import {RequestOptions} from '@angular/http'
import {CookieService} from 'app/services/network/cookie.service'
import {Headers} from '@angular/http'


@Injectable()
export class CsrfService {
    constructor(
        private cookieService: CookieService,
    ) { }

    getRequestOptions(): RequestOptions {
        let headers = new Headers({
            'Content-Type': 'application/json',
            'X-CSRFToken': this.cookieService.getByName('csrftoken'),
        })
        return new RequestOptions({headers: headers})
    }
}
