## DV01 Tech Challenge
### Loan level Cash Flow engine

Main structure

###Class: Loan 

* Loan_base: _term, _current_balance, _rate, _default(bool)
  * monthly_rate()
  * equal_pmt_amt()
  * defaulted()
  * matured()
  
* Loan Pool: _loan_list
  * constructor(loan_list)
  * add loan
  * get waterfall
  
    
* Class: factors
    * prepayment_rate: assume fixed
    * default_rate: assume fixed
    

