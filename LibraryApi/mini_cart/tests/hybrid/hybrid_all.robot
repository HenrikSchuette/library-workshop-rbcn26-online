*** Settings ***
Library    hybrid.minicart_hybrid.MiniCartHybridLibrary    kw_group=all

*** Test Cases ***
All Keywords Are Available
    ${line}=    Add Line Item    10.0    2
    ${sub}=     Sum Line Items   ${line}
    ${disc}=    Apply Discount   ${sub}   10
    ${total}=   Total With Tax   ${disc}  21
    Should Be Equal As Numbers   ${total}   21.78
