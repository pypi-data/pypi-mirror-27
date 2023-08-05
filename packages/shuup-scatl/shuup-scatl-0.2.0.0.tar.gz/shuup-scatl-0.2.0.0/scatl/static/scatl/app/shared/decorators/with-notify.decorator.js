"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
function withNotify(messages) {
    return (target, propertyKey, descriptor) => {
        let originalMethod = descriptor.value;
        descriptor.value = function (...args) {
            let notifyService = this.notifyService;
            let result;
            try {
                result = originalMethod.apply(this, args);
                showSuccessNotify(notifyService, messages);
            }
            catch (error) {
                showErrorNotify(notifyService, messages, error);
            }
            return result;
        };
        return descriptor;
    };
}
exports.withNotify = withNotify;
/** It will break without the semicolons. */
function asyncWithNotify(messages) {
    return (target, propertyKey, descriptor) => {
        let originalMethod = descriptor.value;
        descriptor.value = function (...args) {
            return __awaiter(this, void 0, void 0, function* () {
                let notifyService = this.notifyService;
                let result;
                try {
                    result = yield originalMethod.apply(this, args);
                    showSuccessNotify(notifyService, messages);
                }
                catch (error) {
                    showErrorNotify(notifyService, messages, error);
                }
                return result;
            });
        };
        return descriptor;
    };
}
exports.asyncWithNotify = asyncWithNotify;
function showSuccessNotify(notifyService, messages) {
    if (messages.onSuccessMsg !== undefined) {
        notifyService.success(messages.onSuccessMsg);
    }
}
function showErrorNotify(notifyService, messages, error) {
    let errorMsgBody;
    if (messages.onErrorMsg.body === undefined) {
        errorMsgBody = `${error}`;
    }
    else {
        errorMsgBody = `${messages.onErrorMsg.body}<br>${error}`;
    }
    notifyService.error(messages.onErrorMsg.header, errorMsgBody);
}
//# sourceMappingURL=with-notify.decorator.js.map