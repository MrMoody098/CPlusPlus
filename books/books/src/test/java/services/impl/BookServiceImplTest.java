package services.impl;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

import org.mockito.InjectMocks;
import org.mockito.Mock;

import com.moody.domain.Book;
import com.moody.domain.BookEntity;
import com.moody.repositories.BookRepository;
import com.moody.services.impl.BookServiceImpl;

public class BookServiceImplTest {
    
    @Mock
    private BookRepository bookRepository;
    
    @InjectMocks
    private BookServiceImpl underTest;

    public void testThatBookIsSaved(){
        final Book book = Book.builder().isbn("12345232").Author("yeeuts").title("cherry hill").build();

        final BookEntity bookEntity= BookEntity.builder().isbn("12345232").Author("yeeuts").title("cherry hill").build();
        
        when(bookRepository.save(eq(bookEntity))).thenReturn(bookEntity);

        final Book result = underTest.create(book);
    }
}
