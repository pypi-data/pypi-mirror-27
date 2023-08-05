import {Injectable} from '@angular/core'


@Injectable()
export class CookieService {
    getByName(name: string): Optional<string> {
        let nameNeedle = `${name}=`
        let cookies: Array<string> = document.cookie.split(';')
        for (let cookieStrRaw of cookies) {
            let cookieStr = cookieStrRaw.trim()
            let isCookieNameFound: boolean = cookieStr.search(nameNeedle) === 0
            if (isCookieNameFound) {
                let cookieValueIndexStart = nameNeedle.length
                let cookieValueIndexEnd = cookieStr.length
                let cookieValue = cookieStr.substring(
                    cookieValueIndexStart,
                    cookieValueIndexEnd,
                )
                return cookieValue
            }
        }
        return null
    }
}
