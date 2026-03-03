*** Settings ***
Library    dynamic.minicart_dynamic.MiniCartDynamicLibrary    kw_group=all    AS    all
Library    dynamic.minicart_dynamic.MiniCartDynamicLibrary    kw_group=pricing    AS    PricingOnly

*** Test Cases ***
Dynamic All Keywords Work
    ${line1}=    all.Add Line Item    10.0    2
    ${line2}=    all.Add Line Item    5.0     1
    ${subtotal}=    all.Sum Line Items    ${line1}    ${line2}
    ${discounted}=    all.Apply Discount    ${subtotal}    10
    ${total}=    all.Total With Tax    ${discounted}    21
    Should Be Equal As Numbers    ${total}    27.225

Dynamic Group Filters Keywords
    ${disc}=    PricingOnly.Apply Discount    100    10
    ${taxed}=   PricingOnly.Total With Tax   ${disc}    21
    Should Be Equal As Numbers    ${taxed}    108.9

    Run Keyword And Expect Error    *No keyword with name*Add Line Item*    PricingOnly.Add Line Item    1    1
