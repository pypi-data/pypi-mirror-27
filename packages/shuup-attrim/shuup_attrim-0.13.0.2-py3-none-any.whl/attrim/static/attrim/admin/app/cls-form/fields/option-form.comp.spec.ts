import {FormsModule} from '@angular/forms'
import {async} from '@angular/core/testing'
import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'
import {TransStrComponent} from 'app/cls-form/fields/trans-str.comp'
import {DebugElement} from '@angular/core'
import {OptionFormComponent} from 'app/cls-form/fields/option-form.comp'
import {Type} from 'app/type.enum'
import {By} from '@angular/platform-browser'
import {NotifyService} from 'app/services/notify.service'
import {NotificationsService} from 'angular2-notifications'
import {OptionJsonSerializerService} from 'app/services/network/serializers/option-json.service'
import {OptionNetworkService} from 'app/services/network/option.service'
import {Option} from 'app/models/option.model'
import {CookieService} from 'app/services/network/cookie.service'
import {CsrfService} from 'app/services/network/csrf.service'
import {L_SEMANTIC_UI_MODULE} from 'angular2-semantic-ui'


describe('option tests', () => {
    let self: {
        fixture: ComponentFixture<OptionFormComponent>
        debugElem: DebugElement
        component: OptionFormComponent
    }

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [FormsModule, L_SEMANTIC_UI_MODULE],
            declarations: [OptionFormComponent, TransStrComponent],
            providers: [
                NotifyService, NotificationsService, OptionJsonSerializerService,
                CookieService, CsrfService,
                {provide: OptionNetworkService, useValue: new OptionNetworkServiceStub()},
            ],
        })
        TestBed.compileComponents()
    }))

    beforeEach(() => {
        let fixture = TestBed.createComponent(OptionFormComponent)
        self = {
            fixture: fixture,
            debugElem: fixture.debugElement,
            component: fixture.componentInstance,
        }
    })

    it('syncs the input and value with Type.TRANS_STR', () => {
        self.component.initForm({type: Type.TRANS_STR})

        let input = self.fixture.debugElement.query(By.css('input'))
        let newValue = 'new value'
        input.nativeElement.value = newValue
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        let filledButton = self.debugElem.query(By.css('.checkmark.box'))
        expect(filledButton).not.toBeNull()

        expect(self.component.model.value[window.DJANGO.defaultLang]).toBe(newValue)
    })

    it('syncs the input and value with Type.STR', () => {
        self.component.initForm({type: Type.STR})

        let input = self.fixture.debugElement.query(By.css('input'))
        let newValue = 'new value'
        input.nativeElement.value = newValue
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        expect(self.component.model.value).toBe(newValue)
    })

    it('syncs the input and value with Type.INT', () => {
        self.component.initForm({type: Type.INT})

        let input = self.fixture.debugElement.query(By.css('input'))
        let newValue = '5'
        input.nativeElement.value = newValue
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        let component = self.component
        expect(component.model.value.toString()).toBe(newValue)
    })

    it('syncs the input and value with Type.DECIMAL', () => {
        self.component.initForm({type: Type.DECIMAL})

        let input = self.fixture.debugElement.query(By.css('input'))
        let newValue = '5.5'
        input.nativeElement.value = newValue
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        expect(self.component.model.value.toString()).toBe(newValue)
    })
})


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
