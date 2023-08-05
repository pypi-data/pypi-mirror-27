import {Injectable} from '@angular/core'
import {OptionJsonSerializerService} from 'app/services/network/serializers/option-json.service'
import {Option} from 'app/models/option.model'
import {Http} from '@angular/http'
import {CsrfService} from 'app/services/network/csrf.service'


@Injectable()
export class OptionNetworkService {
    constructor(
        private jsonSerializer: OptionJsonSerializerService,
        private csrfService: CsrfService,
        private http: Http,
    ) { }

    async get(pk: PrimaryKey): Promise<Option> {
        let response = await this.http.get(`/api/attrim/options/${pk}/`)
            .first()
            .toPromise()
        let optionJson = response.json()
        let option = await this.jsonSerializer.deserialize(optionJson)
        return option
    }

    async save(option: Option): Promise<Option> {
        let optionJson = this.jsonSerializer.serialize(option)
        let response = await this.http.patch(
            `/api/attrim/options/${option.pk}/`,
            optionJson, this.csrfService.getRequestOptions(),
        )
            .first()
            .toPromise()
        let optionSavedJson = response.json()
        let optionSaved = await this.jsonSerializer.deserialize(optionSavedJson)
        return optionSaved
    }

    async create(option: Option): Promise<Option> {
        let optionJson = this.jsonSerializer.serialize(option)
        let response = await this.http.post(
            `/api/attrim/options/`,
            optionJson, this.csrfService.getRequestOptions(),
        )
            .first()
            .toPromise()
        let optionCreatedJson = response.json()
        let optionCreated = await this.jsonSerializer.deserialize(optionCreatedJson)
        return optionCreated
    }

    async delete(option: Option) {
        await this.http.delete(
            `/api/attrim/options/${option.pk}/`,
            this.csrfService.getRequestOptions(),
        )
            .first()
            .toPromise()
    }
}
