import {element} from 'protractor'
import {by} from 'protractor'
import {$} from 'protractor'
import {browser} from 'protractor'
import {DJANGO} from './django'


export async function login() {
    await browser.waitForAngularEnabled(false)

    let loginPageUrl = `${DJANGO.url}/sa/login/`
    await browser.driver.get(loginPageUrl)

    let usernameField = $('#id_username')
    await usernameField.sendKeys(DJANGO.user.username)
    let passwordField = $('#id_password')
    await passwordField.sendKeys(DJANGO.user.password)

    let submitButton = $(`button[type="submit"]`)
    await submitButton.click()

    await browser.waitForAngularEnabled(true)
}


export async function loadClsEditForm(clsCode: string = 'language') {
    await browser.waitForAngularEnabled(false)

    await browser.driver.get(`${DJANGO.url}/sa/attrim/`)
    let clsLink = element(by.cssContainingText('#picotable tbody a', clsCode))
    await browser.wait(async () => await clsLink.isPresent())
    await clsLink.click()

    await browser.wait(async () => $('cls-form').isPresent())
    await browser.waitForAngularEnabled(true)
    await browser.waitForAngular()
}


export async function loadClsNewForm() {
    await browser.waitForAngularEnabled(false)

    await browser.driver.get(`${DJANGO.url}/sa/attrim/new/`)

    await browser.wait(async () => $('cls-form').isPresent())
    await browser.waitForAngularEnabled(true)
    await browser.waitForAngular()
}
