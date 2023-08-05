import {Component} from '@angular/core'
import {Type} from 'app/type.enum'
import {OptionFormComponent} from 'app/cls-form/fields/option-form.comp'
import {ComponentFactoryResolver} from '@angular/core'
import {ViewContainerRef} from '@angular/core'
import {ComponentRef, ViewChild} from '@angular/core'
import {TypeEnumDecorator} from 'app/decorators/type.enum.decorator'
import {OnInit, ViewEncapsulation} from '@angular/core'
import {Cls} from 'app/models/cls.model'
import {ClsNetworkService} from 'app/services/network/cls.service'
import {ProductType} from 'app/models/product-type.model'
import {ProductTypeNetworkService} from 'app/services/network/product-type.service'
import {NotifyService} from 'app/services/notify.service'
import {SlimLoadingBarService} from 'ng2-slim-loading-bar'
import {asyncShowLoadingBar} from 'app/decorators/async-show-loading-bar.decorator'
import {asyncNotifyOn} from 'app/decorators/async-notify-on.decorator'


// TODO refactor?
@Component({
    selector: 'cls-form',
    moduleId: module.id,
    templateUrl: 'cls-form.comp.html',
    styleUrls: ['cls-form.comp.css'],
    encapsulation: ViewEncapsulation.None,
})
@TypeEnumDecorator
export class ClsFormComponent implements OnInit {
    // TODO mark the name field as required
    model: Cls
    productTypeList: Array<ProductType>

    optionRefSet: Set<ComponentRef<OptionFormComponent>> = new Set()
    @ViewChild('options', {read: ViewContainerRef})
    private optionsContainerRef: ViewContainerRef

    // noinspection JSUnusedLocalSymbols
    constructor(
        private networkService: ClsNetworkService,
        private productTypeService: ProductTypeNetworkService,
        private notifyService: NotifyService,
        private loadingBarService: SlimLoadingBarService,
        private componentFactoryResolver: ComponentFactoryResolver,
    ) { }

    ngOnInit() {
        let clsStubForRender = new Cls({
            code: '',
            type: Type.INT,
            productType: {name: '', pk: 0},
        })
        this.model = clsStubForRender

        // noinspection JSIgnoredPromiseFromCall
        this.initForm()
    }

    protected setType(typeValueRaw: string) {
        let typeNew: Type = Number(typeValueRaw)
        this.model.type = typeNew
    }

    protected setProductType(productTypePkRaw: string) {
        let pkSelected: PrimaryKey = Number(productTypePkRaw)
        this.model.productType = this.productTypeList
            .find(productType => productType.pk === pkSelected) as ProductType
    }

    protected addOption(args?: {
        optionPk?: PrimaryKey | undefined,
        type?: Type | undefined,
        clsPk?: PrimaryKey | undefined,
    }) {
        let ref: ComponentRef<OptionFormComponent> = this.createOptionComponent()
        if (args) {
            // noinspection JSIgnoredPromiseFromCall
            ref.instance.initForm(args)
        } else {
            // noinspection JSIgnoredPromiseFromCall
            ref.instance.initForm({type: this.model.type, clsPk: this.model.pk})
        }
        this.optionRefSet.add(ref)
    }

    @asyncShowLoadingBar
    @asyncNotifyOn({success: 'The saving complete', error: 'The saving failed'})
    protected async save() {
        let clsSaved = await this.saveCls()
        await this.saveOptions(clsSaved.pk as PrimaryKey)
    }

    @asyncShowLoadingBar
    @asyncNotifyOn({error: 'Creation failed'})
    protected async create() {
        let clsCreated = await this.networkService.create(this.model)
        await this.saveOptions(clsCreated.pk as PrimaryKey)
        location.assign(`/sa/attrim/${clsCreated.pk}/`)
    }

    private async saveCls(): Promise<Cls> {
        let clsSaved: Cls = await this.networkService.save(this.model)
        this.model = clsSaved
        return clsSaved
    }

    private async saveOptions(clsPk: PrimaryKey) {
        let optionSavePromises: Array<Promise<any>> = []
        for (let optionRef of this.optionRefSet) {
            optionRef.instance.model.clsPk = clsPk
            let savePromise = optionRef.instance.save()
            optionSavePromises.push(savePromise)
        }
        await Promise.all(optionSavePromises)
    }

    @asyncShowLoadingBar
    private async initForm() {
        await this.initProductTypeList()
        if (window.DJANGO.isEditForm) {
            await this.loadFormDataFromServer()
        } else {
            this.loadFormDataDefault()
        }
    }

    @asyncNotifyOn({error: 'Network error during product types retrieving'})
    private async initProductTypeList() {
        // TODO use an async pipe with productTypeService.getAll() and remove clsStubForRender
        this.productTypeList = await this.productTypeService.getAll()
    }

    private async loadFormDataFromServer() {
        let clsPkToEdit = window.DJANGO.clsPrimaryKey as PrimaryKey
        let clsToEdit = await this.networkService.get(clsPkToEdit)
        this.model = clsToEdit

        for (let optionPk of clsToEdit.optionsPk) {
            this.addOption({optionPk: optionPk})
        }
    }

    private loadFormDataDefault() {
        let clsDefault = new Cls({
            code: '',
            type: Type.INT,
            productType: this.productTypeList[0],
        })
        this.model = clsDefault
    }

    private createOptionComponent(): ComponentRef<OptionFormComponent> {
        let factory = this.componentFactoryResolver
            .resolveComponentFactory(OptionFormComponent)
        return this.optionsContainerRef.createComponent(factory)
    }
}
