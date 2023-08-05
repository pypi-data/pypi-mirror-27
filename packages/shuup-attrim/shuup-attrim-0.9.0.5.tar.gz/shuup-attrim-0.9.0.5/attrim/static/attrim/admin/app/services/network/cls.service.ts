import {Injectable} from '@angular/core'
import {Cls} from 'app/models/cls.model'
import {ClsJsonSerializerService} from 'app/services/network/serializers/cls-json.service'
import {Http} from '@angular/http'
import {CsrfService} from 'app/services/network/csrf.service'


@Injectable()
export class ClsNetworkService {
    constructor(
        private jsonSerializer: ClsJsonSerializerService,
        private csrfService: CsrfService,
        private http: Http,
    ) { }

    async get(pk: PrimaryKey): Promise<Cls> {
        let response = await this.http.get(`/api/attrim/classes/${pk}/`)
            .first()
            .toPromise()
        let clsJson = response.json()
        let cls = await this.jsonSerializer.deserialize(clsJson)
        return cls
    }

    async save(cls: Cls): Promise<Cls> {
        let clsJson = this.jsonSerializer.serialize(cls)
        let response = await this.http.patch(
            `/api/attrim/classes/${cls.pk}/`,
            clsJson, this.csrfService.getRequestOptions(),
        )
            .first()
            .toPromise()
        let clsSavedJson = response.json()
        let clsSaved = await this.jsonSerializer.deserialize(clsSavedJson)
        return clsSaved
    }

    async create(cls: Cls): Promise<Cls> {
        let clsJson = this.jsonSerializer.serialize(cls)
        let response = await this.http.post(
            `/api/attrim/classes/`,
            clsJson, this.csrfService.getRequestOptions(),
        )
            .first()
            .toPromise()
        let clsJsonCreated = response.json()
        let clsCreated = await this.jsonSerializer.deserialize(clsJsonCreated)
        return clsCreated
    }
}
