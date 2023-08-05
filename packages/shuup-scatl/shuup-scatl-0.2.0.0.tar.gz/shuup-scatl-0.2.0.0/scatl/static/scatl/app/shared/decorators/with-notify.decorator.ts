import {NotifyService} from 'app/shared/notify.service'


export function withNotify(messages: NotifyMessages): Function {
    return (target: Object, propertyKey: string, descriptor: TypedPropertyDescriptor<any>) => {
        let originalMethod = descriptor.value
        descriptor.value = function(...args: any[]): any {
            let notifyService = (this as Notifiable).notifyService
            let result: any
            try {
                result = originalMethod.apply(this, args);
                showSuccessNotify(notifyService, messages);
            } catch (error) {
                showErrorNotify(notifyService, messages, error);
            }
            return result
        }
        return descriptor
    }
}


/** It will break without the semicolons. */
export function asyncWithNotify(messages: NotifyMessages): Function {
    return (target: Object, propertyKey: string, descriptor: TypedPropertyDescriptor<any>) => {
        let originalMethod = descriptor.value
        descriptor.value = async function(...args: any[]): Promise<any> {
            let notifyService = (this as Notifiable).notifyService
            let result: any
            try {
                result = await originalMethod.apply(this, args);
                showSuccessNotify(notifyService, messages);
            } catch (error) {
                showErrorNotify(notifyService, messages, error);
            }
            return result
        }
        return descriptor
    }
}


export interface NotifyMessages {
    onSuccessMsg?: string
    onErrorMsg: {
        header: string
        body?: string
    }
}


export interface Notifiable {
    notifyService: NotifyService
}


function showSuccessNotify(notifyService: NotifyService, messages: NotifyMessages) {
    if (messages.onSuccessMsg !== undefined) {
        notifyService.success(messages.onSuccessMsg)
    }
}


function showErrorNotify(notifyService: NotifyService, messages: NotifyMessages, error: Error) {
    let errorMsgBody: string
    if (messages.onErrorMsg.body === undefined) {
        errorMsgBody = `${error}`
    } else {
        errorMsgBody = `${messages.onErrorMsg.body}<br>${error}`
    }
    notifyService.error(messages.onErrorMsg.header, errorMsgBody)
}
