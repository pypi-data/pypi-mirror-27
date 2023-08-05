import {browser} from 'protractor'
import {login} from './navigation'


export async function init() {
    await login()
    // otherwise shuup may switch to a mobile makeup and protractor testing will
    // become even more nasty
    await browser.driver.manage().window().setSize(1900, 1000)
}
