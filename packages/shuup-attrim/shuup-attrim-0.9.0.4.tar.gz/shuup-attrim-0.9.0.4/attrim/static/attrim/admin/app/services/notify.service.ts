import {Injectable} from '@angular/core'

import {NotificationsService} from 'angular2-notifications'


@Injectable()
export class NotifyService {
    private service: NotificationsService

    private config = {
        timeOut: 5000,
        showProgressBar: true,
        pauseOnHover: true,
        clickToClose: true,
    }

    constructor(service: NotificationsService) {
        this.service = service
    }

    error(title: string, content: string = '') {
        this.service.error(title, content, this.config)
    }

    success(title: string, content: string = '') {
        this.service.success(title, content, this.config)
    }
}
