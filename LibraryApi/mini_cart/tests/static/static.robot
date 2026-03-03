*** Settings ***
Library    static.minicart_static.MiniCartLibrary

*** Test Cases ***
Complete Pricing Flow
    ${line1}=    Add Line Item    10.0    2
    ${line2}=    Add Line Item    5.0     1
    ${subtotal}=    Sum Line Items    ${line1}    ${line2}
    ${discounted}=    Apply Discount    ${subtotal}    10
    ${total}=    Total With Tax    ${discounted}    21
    Should Be Equal As Numbers    ${total}    27.225

Negative Quantity Should Fail
    Run Keyword And Expect Error    *Quantity cannot be negative*    Add Line Item    10    -1

Invalid Discount Should Fail
    Run Keyword And Expect Error    *Discount percent must be between 0 and 100*    Apply Discount    100    150
