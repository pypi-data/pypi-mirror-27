import {FormsModule} from '@angular/forms'
import {async} from '@angular/core/testing'
import {By, BrowserModule} from '@angular/platform-browser'
import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'
import {DebugElement} from '@angular/core'
import {ClsFormComponent} from 'app/cls-form/cls-form.comp'
import {OptionFormComponent} from 'app/cls-form/fields/option-form.comp'
import {TransStrComponent} from 'app/cls-form/fields/trans-str.comp'
import {NgModule} from '@angular/core'
import {Option} from 'app/models/option.model'
import {Cls} from 'app/models/cls.model'
import {Type} from 'app/type.enum'
import {ClsNetworkService} from 'app/services/network/cls.service'
import {IterateEnumPipe} from 'app/iter-enum.pipe'
import {ClsJsonSerializerService} from 'app/services/network/serializers/cls-json.service'
import {ProductTypeNetworkService} from 'app/services/network/product-type.service'
import {ProductType} from 'app/models/product-type.model'
import {NotifyService} from 'app/services/notify.service'
import {NotificationsService} from 'angular2-notifications'
import {SlimLoadingBarModule} from 'ng2-slim-loading-bar'
import {OptionJsonSerializerService} from 'app/services/network/serializers/option-json.service'
import {OptionNetworkService} from 'app/services/network/option.service'
import {ProductTypeJsonSerializerService} from 'app/services/network/serializers/product-type-json.service'
import {HttpModule} from '@angular/http'
import {CookieService} from 'app/services/network/cookie.service'
import {CsrfService} from 'app/services/network/csrf.service'
import {SimpleNotificationsModule} from 'angular2-notifications'
import {L_SEMANTIC_UI_MODULE} from 'angular2-semantic-ui'


describe('cls form tests', () => {
    let self: {
        fixture: ComponentFixture<ClsFormComponent>
        debugElem: DebugElement
        component: ClsFormComponent
    }

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [FakeModule],
        })
        TestBed.compileComponents()
    }))

    beforeEach(() => {
        initTestCase()
        resetTypeInput()
    })

    it('can handle name update', () => {
        let clsNameSection = self.debugElem.query(By.css('#cls-name'))
        let input = clsNameSection.query(By.css('input'))
        input.nativeElement.value = 'new value'
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        let updatedButtonClass = '.checkmark.box'
        let updatedButton = clsNameSection.query(By.css(updatedButtonClass))
        expect(updatedButton).not.toBeNull()
    })

    it('can handle product type update', async done => {
        // wait for the fake network request
        await self.fixture.whenStable()

        self.component.productTypeList = [
            new ProductType(1, 'test name 1'),
            new ProductType(2, 'test name 2'),
        ]
        self.fixture.detectChanges()

        let productTypeToSelect = self.component.productTypeList[1]
        expect(self.component.model.productType).not.toBe(productTypeToSelect)
        let productTypeSelectInput = self.debugElem.query(By.css('#cls-product-type select'))
        productTypeSelectInput.nativeElement.value = productTypeToSelect.pk
        productTypeSelectInput.nativeElement.dispatchEvent(new Event('change'))
        expect(self.component.model.productType).toBe(productTypeToSelect)
        done()
    })

    it('updates the option-form trans-str buttons status an on input change', () => {
        self.component.addOption()
        self.component.addOption()

        let input = self.debugElem.query(By.css('option-form trans-str input'))
        input.nativeElement.value = 'new value'
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        let updatedButtonClass = '.checkmark.box'
        let updatedButton = self.debugElem.query(By.css(updatedButtonClass))
        expect(updatedButton).not.toBeNull()
    })

    function initTestCase() {
        let fixture = TestBed.createComponent(ClsFormComponent)
        self = {
            fixture: fixture,
            component: fixture.componentInstance,
            debugElem: fixture.debugElement,
        }
        self.fixture.detectChanges()
    }

    function resetTypeInput() {
        let selectInput = self.debugElem.query(By.css('#cls-type select'))
        selectInput.nativeElement.value = Type.TRANS_STR
        selectInput.nativeElement.dispatchEvent(new Event('change'))
    }
})


class ClsNetworkServiceStub {
    async get(pk: PrimaryKey): Promise<Cls> {
        let cls = new Cls({
            code: 'test mock',
            type: Type.TRANS_STR,
            name: {
                en: 'english name',
                fi: 'not en name',
            },
            productType: {name: 'test', pk: 1},
        })
        return cls
    }
}


class ProductTypeNetworkServiceStub {
    async get(pk: PrimaryKey): Promise<ProductType> {
        return {name: 'Mock product type', pk: 1}
    }
    //noinspection JSUnusedGlobalSymbols
    async getAll(): Promise<Array<ProductType>> {
        return [{name: 'Mock product type', pk: 1}]
    }
}


class OptionNetworkServiceStub {
    async get(pk: PrimaryKey): Promise<Option> {
        return new Option({
            pk: pk,
            clsPk: 1,
            type: Type.TRANS_STR,
            isSaved: true,
        })
    }
    async save(option: Option): Promise<Option> {
        return {} as any
    }
}


/**
 * The `configureTestingModule` method does not support `entryComponents` in
 * angular 4.0.3, so they must be included through a fake module.
 */
@NgModule({
    imports: [
        BrowserModule, FormsModule, HttpModule, SlimLoadingBarModule.forRoot(),
        SimpleNotificationsModule.forRoot(), L_SEMANTIC_UI_MODULE,
    ],
    declarations: [ClsFormComponent, OptionFormComponent, TransStrComponent, IterateEnumPipe],
    entryComponents: [OptionFormComponent],
    exports: [IterateEnumPipe],
    providers: [
        ClsNetworkService, ClsJsonSerializerService,
        ProductTypeNetworkService, NotifyService, NotificationsService,
        OptionJsonSerializerService, CsrfService,
        ProductTypeJsonSerializerService, CookieService,
        {provide: OptionNetworkService, useValue: new OptionNetworkServiceStub()},
        {provide: ClsNetworkService, useValue: new ClsNetworkServiceStub()},
        {provide: ProductTypeNetworkService, useValue: new ProductTypeNetworkServiceStub()},
    ],
})
class FakeModule { }
