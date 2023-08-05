import {Component} from '@angular/core'
import {TypeEnumDecorator} from 'app/decorators/type.enum.decorator'
import {Type} from 'app/type.enum'
import {ChangeDetectorRef} from '@angular/core'
import {Option} from 'app/models/option.model'
import {OptionNetworkService} from 'app/services/network/option.service'
import {ViewEncapsulation} from '@angular/core'


@Component({
    selector: 'option-form',
    moduleId: module.id,
    templateUrl: 'option-form.comp.html',
    styleUrls: ['option-form.comp.css'],
    // the encapsulation is screwed up for dynamic components in 4.0.3
    encapsulation: ViewEncapsulation.None,
})
@TypeEnumDecorator
export class OptionFormComponent {
    model: Option

    isCanBeRestored: boolean = true

    constructor(
        private networkService: OptionNetworkService,
        private changeDetector: ChangeDetectorRef,
    ) { }

    async initForm(args: {
        optionPk?: PrimaryKey | undefined,
        type?: Type | undefined,
        clsPk?: PrimaryKey | undefined | null,
    }) {
        this.initChildComponents()

        let option: Option
        if (args.optionPk !== undefined) {
            option = await this.networkService.get(args.optionPk)
        } else {
            option = new Option({type: args.type as Type, clsPk: args.clsPk})
        }
        this.model = option

        this.updateNgSwitch()
    }

    setOrder(valueRaw: string) {
        this.model.order = Number(valueRaw)
    }

    async save() {
        if (this.model.isMarkedAsRemoved) {
            await this.networkService.delete(this.model)
            this.isCanBeRestored = false
        } else if (this.model.isSaved) {
            let optionSaved = await this.networkService.save(this.model)
            this.model = optionSaved
        } else {
            let optionCreated = await this.networkService.create(this.model)
            this.model = optionCreated
        }
    }

    /**
     * For TRANS_STR init, also required if it's an edit form and the edited Option
     * has TRANS_STR type. Otherwise the ngModel binding won't work.
     */
    private initChildComponents() {
        this.model = new Option({type: Type.TRANS_STR})
        this.changeDetector.detectChanges()
    }

    private updateNgSwitch() {
        this.changeDetector.detectChanges()
    }
}
