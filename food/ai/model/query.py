from .statement import Statement


class Query:
    """
    Make your instruction more explicit
    Specify the format you want the answer in
    Ask the model to think step by step or debate pros and cons before settling on an answer

    You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: {knowledge_cutoff} Current date: {current_date}
    """

    def __init__(self, statements: list[Statement]) -> None:
        system_statement_count = len([x for x in statements if x.role == Statement.Role.SYSTEM])
        if system_statement_count > 1:
            raise ValueError(f"System statement is only allowed 1 or 0. Got {statements}")
        elif system_statement_count == 1 and statements[0].role != Statement.Role.SYSTEM:
            raise ValueError(f"System statement should be in the first of statements. Got {statements}")
        self.statements = statements

    @property
    def value(self):
        return [x.query_form for x in self.statements]

    def append(self, statement: Statement) -> None:
        if self.statements and statement.role == Statement.Role.SYSTEM:
            raise ValueError(f"System statement is only allowed in the first of statements")
        self.statements.append(statement)
